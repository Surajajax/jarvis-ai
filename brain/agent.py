from brain.llm import ask_jarvis
from tools.calculator import calculate
from tools.web_search import web_search


# ============================================
# CALCULATOR DETECTION
# ============================================

def is_calculation(text):
    text = text.lower().strip()

    math_symbols = [
        "+",
        "*",
        "/",
        "%"
    ]

    math_words = [
        "plus",
        "minus",
        "multiplied by",
        "multiply by",
        "times",
        "divided by",
    ]

    if any(symbol in text for symbol in math_symbols):
        return True

    if any(word in text for word in math_words):
        return True

    if text.startswith("calculate"):
        return True

    return False


# ============================================
# PREPARE CALCULATION
# ============================================

def prepare_calculation(text):
    text = text.lower().strip()

    replacements = {
        "please calculate": "",
        "calculate": "",
        "what is": "",
        "how much is": "",

        "multiplied by": "*",
        "multiply by": "*",
        "times": "*",

        "divided by": "/",

        "plus": "+",
        "minus": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


# ============================================
# WEB SEARCH DETECTION
# ============================================

def needs_web_search(text):
    text = text.lower().strip()

    web_keywords = [
        "latest",
        "today",
        "current",
        "recent",
        "news",
        "who is",
        "who was",
        "what happened",
        "when is",
        "where is",
        "how many",
        "how much does",
        "score",
        "price",
        "stock",
        "trending",
    ]

    return any(
        keyword in text
        for keyword in web_keywords
    )


# ============================================
# WEB SEARCH ANSWER
# ============================================

def answer_from_web(user_text):
    print("\n🌐 Searching the web...")

    search_results = web_search(user_text)

    if search_results.startswith("Web search error"):
        return search_results

    return search_results


# ============================================
# MAIN JARVIS AGENT
# ============================================

def jarvis_agent(user_text):

    user_text = user_text.strip()

    if not user_text:
        return "I didn't hear anything."

    # ========================================
    # 1. CALCULATOR
    # ========================================

    if is_calculation(user_text):

        expression = prepare_calculation(user_text)

        result = calculate(expression)

        if "couldn't calculate" not in result.lower():
            return f"The answer is {result}."

    # ========================================
    # 2. WEB SEARCH
    # ========================================

    if needs_web_search(user_text):

        return answer_from_web(user_text)

    # ========================================
    # 3. LOCAL QWEN LLM
    # ========================================

    return ask_jarvis(user_text)


# ============================================
# AGENT TEST
# ============================================

if __name__ == "__main__":

    print("🤖 JARVIS AGENT TEST")
    print("====================")

    while True:

        try:

            user_text = input("\nYou: ").strip()

            # Exit commands
            if user_text.lower() in [
                "exit",
                "quit",
                "stop"
            ]:

                print("\n🛑 Agent stopped.")
                break

            # Run agent
            response = jarvis_agent(user_text)

            # Display response
            print(f"\n🤖 JARVIS: {response}")

        except KeyboardInterrupt:

            print("\n\n🛑 Agent stopped.")
            break

        except Exception as e:

            print(f"\n❌ Error: {e}")