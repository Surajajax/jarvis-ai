import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    raise ValueError(
        "TAVILY_API_KEY not found in .env"
    )


client = TavilyClient(
    api_key=API_KEY
)


def web_search(query):
    try:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_answer=True
        )

        answer = response.get("answer")

        if answer:
            return answer

        results = response.get("results", [])

        if not results:
            return "No search results found."

        return results[0].get(
            "content",
            "No useful information found."
        )

    except Exception as e:

        return f"Web search error: {e}"


if __name__ == "__main__":

    print("🌐 Tavily Web Search Test")
    print("==========================")

    query = input("\nSearch: ")

    result = web_search(query)

    print("\n==========================")
    print(result)
    print("==========================")