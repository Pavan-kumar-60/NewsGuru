from langchain_community.tools.tavily_search import TavilySearchResults


def get_latest_news(topic):
    search = TavilySearchResults()
    result = search.run(f"{topic}")
    return result
