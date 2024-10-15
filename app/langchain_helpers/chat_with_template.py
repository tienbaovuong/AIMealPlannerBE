from custom_query_retriever import llm

INTENTION_TEMPLATE = """
    You are a helpful assistant. You will be given a message from user.
    Your task is to determine the intention of the user.
    The intention can ONLY be one of the following:
    - MEAL_SUGGESTION: The user wants to get meal suggestion.
    - OTHER: Anything else.

    Return the intention in string format.
    Example 1:
    - Message: I want to eat something with cabbage
    - Intention: MEAL_SUGGESTION

    Example 2:
    - Message: I want to watch a movie
    - Intention: OTHER

    Message: {message}
    Intention:
    """

CHAT_TEMPLATE = """
    You are a helpful assistant. You will be given a message from the user and a list of meals that match the user's request.
    Your task is to generate a SHORT response explain to the user how the meals match the user's request.

    Return the response in string format.

    Example 1:
    - Message: I want to eat something with cabbage
    - Meals: Cabbage soup, Cabbage salad
    - Response: With your request for recipes with cabbage, I found these options for you: Cabbage soup and Cabbage salad. They both use cabbage as the main ingredient and are easy to make.

    Message: {user_message}
    Meals: {meal_titles}
    Response:
    """

async def get_chat_intentions(message: str):
    prompt = INTENTION_TEMPLATE.format(message=message)
    result = await llm.ainvoke(prompt)
    return result.content

async def get_chat_response(user_message: str, meal_titles: str):
    prompt = CHAT_TEMPLATE.format(user_message=user_message, meal_titles=meal_titles)
    result = await llm.ainvoke(prompt)
    return result.content

async def stream_chat_response(user_message: str, meal_titles: str):
    prompt = CHAT_TEMPLATE.format(user_message=user_message, meal_titles=meal_titles)
    async for chunk in await llm.astream(prompt):
        yield chunk.content
