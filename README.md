# AI News Multi-Agent System

This project is a Streamlit web application that demonstrates a multi-agent system for fetching the latest AI news, summarizing the articles, and formatting the summary for presentation. The system uses the Tavily Search API to retrieve current news articles and a local Llama3.2 model (via LangChain Ollama integration) for both summarization and formatting.

## Overview

The application implements a three-step pipeline:

1. **Search Agent:** Retrieves AI news articles using the Tavily Search API (filtered by topic "news", recent articles, etc.) and concatenates the titles and content.
2. **Summarization Agent:** Summarizes the concatenated article text using a local Llama3.2 model.
3. **Formatting Agent:** Formats the summary with clear headings and bullet points for improved readability.

A helper function is provided to extract the final content from the model’s output, ensuring only the desired text is rendered in the UI.

## Features

- **Real-time AI News Retrieval:** Uses Tavily's API to fetch the latest AI news.
- **Text Summarization:** Summarizes news articles using a local Llama3.2 model.
- **Result Formatting:** Formats the summary for clear and concise presentation.
- **Interactive UI:** A Streamlit-based interface for entering a query and viewing the formatted summary.

## Requirements

- Python 3.8 or later
- [Streamlit](https://streamlit.io)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [langchain](https://github.com/hwchase17/langchain)
- [langchain-ollama](https://github.com/hwchase17/langchain-ollama)
- [langchain-community](https://github.com/langchain-ai/langchain-community)
- A valid Tavily API key

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Selim321/ai-news-multi-agent.git
   cd ai-news-multi-agent
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the Required Packages:**

   If a `requirements.txt` is available, run:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install the dependencies manually:

   ```bash
   pip install streamlit python-dotenv langchain langchain-ollama langchain-community
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the project root with the following content:

   ```env
   TAVILY_API_KEY=tvly-YOUR_API_KEY
   ```

## Usage

1. **Run the Streamlit App:**

   ```bash
   streamlit run app.py
   ```

2. **In the Web Interface:**

   - Enter a topic in the text box (e.g., "latest AI news 2025"). If left blank, a default query is used.
   - Click **"Fetch News"**.
   - The app will fetch recent AI news articles, summarize them, format the summary, and display the final output.

## How It Works

### Step 1: Search Agent

- **Function:** `get_articles_text(query: str)`
- **Process:** Calls the Tavily Search API with the topic `"news"`, retrieving articles from the last day (up to 5 results). It concatenates each article’s title and content into one text block.

### Step 2: Summarization Agent

- **Function:** `summarize_text(articles_text: str)`
- **Process:** Builds a prompt with the concatenated articles text and uses the local Llama3.2 model (via `llm.invoke()`) to generate a concise summary.

### Step 3: Formatting Agent

- **Function:** `format_summary(summary: str)`
- **Process:** Constructs a prompt that instructs the model to format the summary with clear headings and bullet points. A helper function `extract_content(formatted_text)` extracts the desired text for presentation.

### UI Pipeline Execution

The Streamlit interface sequentially calls:

1. The **search function** to retrieve and combine articles.
2. The **summarization function** to produce a summary.
3. The **formatting function** to produce a neatly formatted summary.
4. The output is then displayed as Markdown in the UI.

## Project Structure

```
ai-news-multi-agent/
├── app.py              # Main Streamlit application code
├── .env                # Environment variables file (contains Tavily API key)
├── README.md           # Project documentation (this file)
└── requirements.txt    # (Optional) List of required Python packages
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

