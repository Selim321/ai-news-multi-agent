import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    st.error("Tavily API key not found. Please set it in the .env file.")
    st.stop()

# Initialize the Tavily Search tool correctly
search_tool = TavilySearchResults()

# Initialize Ollama with the correct model name
llm = ChatOllama(model="llama3.2")  # Change this to a valid model name

# Memory to store conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define LangChain Agent properly
agent = initialize_agent(
    tools=[search_tool],  # Use the correctly initialized search tool
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Streamlit UI
st.title("📰 AI News Summarizer")

query = st.text_input("Enter a topic (or leave blank for general AI news)", "latest AI news")

if st.button("Fetch News"):
    with st.spinner("Searching & Summarizing..."):
        try:
            response = agent.run(query)
            st.subheader("Summary:")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
