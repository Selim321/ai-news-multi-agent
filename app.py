import streamlit as st
import os
import re
from dotenv import load_dotenv
from langchain_ollama import ChatOllama  # from langchain-ollama package
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    st.error("Tavily API key not found. Please set it in the .env file.")
    st.stop()

# Initialize the local LLM using your local llama3.2 model.
llm = ChatOllama(model="llama3.2", temperature=0)

# Initialize the Tavily Search tool instance.
tavily_search_instance = TavilySearchResults(api_key=TAVILY_API_KEY)

# ---------- Step 1: Search Function ----------
def get_articles_text(query: str) -> str:
    """
    Retrieve articles using the Tavily Search API with topic "news" (last day, max 5 results)
    and concatenate the titles and content.
    """
    results = tavily_search_instance.run(query, topic="news", days=1, max_results=5)
    if isinstance(results, dict):
        articles = results.get("results", [])
    elif isinstance(results, list):
        articles = results
    else:
        articles = []
    
    if not articles:
        return ""
    
    articles_text = "\n\n".join(
        [
            f"Title: {article.get('title', 'No title')}\nContent: {article.get('content', 'No content available.')}"
            for article in articles
        ]
    )
    return articles_text

# ---------- Step 2: Summarization Function ----------
def summarize_text(articles_text: str) -> str:
    """
    Summarize the provided articles text using the local Llama3.2 model.
    """
    prompt = f"Summarize the following AI news articles concisely:\n\n{articles_text}"
    summary = llm.invoke(prompt)
    return summary

# ---------- Step 3: Formatting Function ----------
def format_summary(summary: str) -> str:
    """
    Format the summary with clear headings and bullet points for better readability.
    """
    prompt = f"Format the following summary with clear headings and bullet points for presentation:\n\n{summary}"
    formatted = llm.invoke(prompt)
    return formatted

# Helper function to extract text content from the formatted output.
def extract_content(formatted_text) -> str:
    """
    If formatted_text is an AIMessage or an object with a 'content' attribute, extract that.
    Then, extract the text following 'content="' and before the next '"' if present.
    Otherwise, return the original text.
    """
    # If the object has a content attribute, use it.
    if hasattr(formatted_text, "content"):
        formatted_text = formatted_text.content
    # Ensure we are working with a string.
    formatted_text = str(formatted_text)
    match = re.search(r'content="([^"]+)"', formatted_text)
    if match:
        return match.group(1)
    return formatted_text

# ---------- Streamlit UI ----------
st.title("📰 AI News Multi-Agent System")

query = st.text_input("Enter a topic", "latest AI news 2025")

if st.button("Fetch News"):
    with st.spinner("Fetching articles, summarizing, and formatting..."):
        articles_text = get_articles_text(query)
        if not articles_text:
            st.error("No articles found. Please try a different query.")
        else:
            summary = summarize_text(articles_text)
            formatted_summary = format_summary(summary)
            
            # Extract the actual content from formatted_summary.
            output = extract_content(formatted_summary)
            
            st.subheader("Formatted Summary:")
            st.markdown(output)
