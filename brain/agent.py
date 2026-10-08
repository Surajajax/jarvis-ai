from brain.llm import ask_jarvis
from tools.calculator import calculate
from tools.web_search import web_search


def jarvis_agent(user_text):

    text = user_text.lower().strip()

    # ==============================
    # CALCULATOR
    # ==============================

    calculator_words = [
        "calculate",
        "what is",
        "how much is",
        "plus",
        "minus",
        "multiply",
        "divided by",
        "times",
        "percent",
        "%",
    ]

    has_math_symbol = any(
        symbol in text
        for symbol in ["+", "-", "*", "/", "%"]
    )

    has_calculator_word = any(
        word in text
        for word in calculator_words
    )

    if has_math_symbol or has_calculator_word:

        # Try calculator only when the
        # expression looks mathematical.

        expression = (
            text
            .replace("calculate", "")
            .replace("what is", "")
            .replace("how much is", "")
            .replace("plus", "+")
            .replace("minus", "-")
            .replace("multiply", "*")
            .replace("times", "*")
            .replace("divided by", "/")
            .replace("percent", "%")
        )

        try:

            result = calculate(
                expression.strip()
            )

            if "couldn't calculate" not in result.lower():

                return (
                    f"The answer is {result}."
                )

        except Exception:
            pass

    # ==============================
    # WEB SEARCH
    # ==============================

    web_words = [
        "who is",
        "who was",
        "what happened",
        "latest",
        "today",
        "current",
        "recent",
        "news",
        "when is",
        "where is",
        "how many",
        "score",
        "price",
        "stock",
        "weather",
    ]

    needs_web_search = any(
        word in text
        for word in web_words
    )

    if needs_web_search:

        search_results = web_search(
            user_text
        )

        prompt = f"""
You are JARVIS.

Answer the user's question using
the web search results below.

User question:
{user_text}

Web search results:
{search_results}

Give a concise and accurate answer.
Do not mention that you are reading search results.
"""

        return ask_jarvis(prompt)

    # ==============================
    # NORMAL LLM
    # ==============================

    return ask_jarvis(user_text)


if __name__ == "__main__":

    print("🤖 JARVIS AGENT TEST")
    print("====================")

    while True:

        user_text = input(
            "\nYou: "
        )

        if user_text.lower() in [
            "exit",
            "quit",
        ]:

            break

        response = jarvis_agent(
            user_text
        )

        print(
            f"\nJARVIS: {response}"
        )