from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if "hello" in lowered:
        return "Hello there!"
    if "goodbye" in lowered:
        return "Bye-bye!"
    if "thank" in lowered:
        return "You're welcome!"
    if "how are you" in lowered:
        return "I'm doing well, thank you for asking!"
    if "what's the weather" in lowered:
        return "I'm sorry, I don't know the weather."
    if "what's the time" in lowered:
        return "I'm sorry, I don't know the time."
    if "what's the date" in lowered:
        return "I'm sorry, I don't know the date."
