# 🚀 ByteBrief - AI-Powered Tech Trend Digest

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Powered-green)](https://www.crewai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**ByteBrief** is an AI-powered system that automatically discovers, summarizes, and archives trending tech topics into engaging Twitter threads. Stay ahead of the curve without lifting a finger!

## 🌟 Key Features

- **🤖 AI Crew**: A team of specialized AI agents working together
- **🔍 Trend Discovery**: Automatically finds trending tech topics
- **📝 Smart Summarization**: Converts complex news into digestible bullet points
- **🐦 Twitter-Ready Threads**: Crafts engaging 2-tweet threads for social media
- **📚 Google Docs Archiving**: Automatically saves all threads for future reference
- **⚡ Real-time Updates**: Always stay current with the latest tech developments

## 🤖 Meet the AI Crew

| Agent | Role | Specialization |
|-------|------|----------------|
| **Tech Trend Scraper** | Researcher | Finds 3-5 trending tech topics daily |
| **Trend Summarizer** | Editor | Converts findings into concise bullet points |
| **Tech Thread Writer** | Copywriter | Crafts engaging Twitter threads |
| **Thread Publisher** | Archivist | Saves threads to Google Docs |

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Google Cloud account with Docs API enabled
- API keys for Gemini and Serper

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bytebrief.git
   cd bytebrief
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   SERPER_API_KEY=your_serper_api_key
   GOOGLE_DOC_ID=your_google_doc_id  # Optional
   ```

### Usage

Run ByteBrief to generate and archive your first tech thread:

```bash
python bytebrief_crew.py
```

Watch as the AI crew:
1. Discovers trending tech topics
2. Summarizes them into concise points
3. Crafts engaging Twitter threads
4. Archives them in your Google Doc

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Gemini API key for LLM | ✅ |
| `SERPER_API_KEY` | Serper.dev API key for search | ✅ |
| `GOOGLE_DOC_ID` | Fixed Google Doc ID (optional) | ❌ |

## 📁 Project Structure

```
bytebrief/
├── bytebrief_crew.py     # Main AI crew orchestration
├── google_docs_tool.py   # Google Docs integration tool
├── setup_google_docs.py  # Google Docs setup wizard
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not included)
└── credentials.json     # Google OAuth credentials (not included)
```

## 🧠 How It Works

1. **Discovery Phase**: The Trend Scraper agent searches the web for trending tech topics
2. **Summarization Phase**: The Trend Summarizer refines findings into tweet-friendly content
3. **Creation Phase**: The Thread Writer crafts engaging 2-tweet threads
4. **Archiving Phase**: The Thread Publisher saves threads to Google Docs with timestamps

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Add new AI agents

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) for the amazing multi-agent framework
- [Google Docs API](https://developers.google.com/docs) for seamless document integration
- [Serper.dev](https://serper.dev/) for reliable search capabilities

---

<p align="center">
  Made with ❤️ and ☕ by tech enthusiasts
</p>
