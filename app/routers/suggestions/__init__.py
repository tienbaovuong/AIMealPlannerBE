from . import meal_suggestion,  chat_meal_suggestion

meal_suggestion_routes = [
    meal_suggestion.router,
    chat_meal_suggestion.router,
]