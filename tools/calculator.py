def calculate(expression):
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "I couldn't calculate that."


if __name__ == "__main__":

    print("🧮 Calculator Test")

    expression = input("Enter calculation: ")

    result = calculate(expression)

    print("Result:", result)