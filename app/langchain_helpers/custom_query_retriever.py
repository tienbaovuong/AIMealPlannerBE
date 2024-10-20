from typing import List
import logging
import os

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI

from app.settings.app_settings import AppSettings
from app.models.user_seen_meals import UserSeenMeals

logger = logging.getLogger(__name__)
class CustomSelfQueryRetriever(SelfQueryRetriever):
    def _get_relevant_documents(self, query, run_manager, **kwargs) -> List[Document]:
        structured_query = self.query_constructor.invoke(
            {"query": query}, config={"callbacks": run_manager.get_child()}
        )
        if self.verbose:
            logger.info(f"Generated Query: {structured_query}")
        new_query, search_kwargs = self._prepare_query(query, structured_query)
        exclude_ids = kwargs.pop("exclude_ids", None)
        if exclude_ids:
            exclude_ids_query = {"bool": {"must_not": {"ids": {"values": exclude_ids}}}}
            if "filter" not in search_kwargs:
                search_kwargs["filter"] = []
            search_kwargs["filter"].append(exclude_ids_query)
        docs = self._get_docs_with_query(new_query, search_kwargs)
        return docs
    
    async def _aget_relevant_documents(self, query, run_manager, **kwargs) -> List[Document]:
        structured_query = await self.query_constructor.ainvoke(
            {"query": query}, config={"callbacks": run_manager.get_child()}
        )
        if self.verbose:
            logger.info(f"Generated Query: {structured_query}")
        new_query, search_kwargs = self._prepare_query(query, structured_query)
        exclude_ids = kwargs.pop("exclude_ids", None)
        if exclude_ids:
            exclude_ids_query = {"bool": {"must_not": {"ids": {"values": exclude_ids}}}}
            if "filter" not in search_kwargs:
                search_kwargs["filter"] = []
            search_kwargs["filter"].append(exclude_ids_query)
        docs = await self._aget_docs_with_query(new_query, search_kwargs)
        if (len(docs) == 0 and exclude_ids):
            logger.info(f"No documents found, retry with no ids filter")
            search_kwargs["filter"].pop()
            # Reset user seen meal
            user_id = kwargs.pop("user_id", None)
            if user_id:
                user_seen_meals = UserSeenMeals.find_one({"user_id": user_id})
                await user_seen_meals.delete()
            docs = await self._aget_docs_with_query(new_query, search_kwargs)
        return docs
    
# Get embedding models
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Get Elasticsearch store
app_settings = AppSettings()
vector_store = ElasticsearchStore(
    "meal-recipe", embedding=embeddings, es_url=app_settings.elasticsearch_dsn,
    es_api_key=os.environ['ELASTICSEARCH_API_KEY'],
)

# Get Llama LLM
llm = ChatOpenAI(openai_api_base="https://api.llama-api.com", model="llama3-70b")

# Create self query retriever
metadata_field_info = [
    AttributeInfo(
        name="calories",
        description="The caloric value of the meal",
        type="float",
    ),
    AttributeInfo(
        name="ingredients",
        description="The ingredients of the meal",
        type="list of strings",
    )
]
document_content_description = "Meal recipe information"
retriever = CustomSelfQueryRetriever.from_llm(
    llm, vector_store, document_content_description, metadata_field_info, verbose=True, use_original_query=False,
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.4, "k": 3}, 
    _expects_other_args=True, _new_arg_supported=True
)