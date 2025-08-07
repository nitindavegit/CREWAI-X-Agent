from dotenv import load_dotenv
load_dotenv()

import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from google_docs_tool import GoogleDocsTool

# === Setup Gemini LLM ===
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.3
)

# === Tools ===
search_tool = SerperDevTool()
docs_tool = GoogleDocsTool()

# Check if Google Docs is properly configured
if not os.path.exists('credentials.json'):
    print("⚠️  WARNING: credentials.json not found!")
    print(docs_tool.get_setup_instructions())
    print("\n" + "="*60)

# === Agents ===
trend_scraper = Agent(
    role="Tech Trend Scraper",
    goal="Search and collect 3-5 trending and recent updates in the tech world",
    backstory="You are great at spotting trending tech topics by searching multiple online sources like Google and filtering noise.",
    verbose=True,
    tools=[search_tool],
    llm=llm
)

trend_summarizer = Agent(
    role="Trend Summarizer", 
    goal="Summarize collected trends into short key points",
    backstory="You are skilled at converting tech news into digestible bullets for Twitter readers.",
    verbose=True,
    llm=llm
)

thread_writer = Agent(
    role="Tech Thread Writer",
    goal="Write a 2-tweet Twitter thread labeled as 'Tweet 1:' and 'Tweet 2:'. Start with a hook tweet and follow-up with value-add tweet(s). Do NOT use 1/2 or 2/2 format.",
    backstory="You're an expert in writing short, impactful Twitter threads to educate and engage the tech community.",
    verbose=True,
    llm=llm
)

thread_publisher = Agent(
    role="Thread Publisher",
    goal="Save the tweet thread to a fixed Google Docs archive",
    backstory="You're the last step in ByteBrief — archive every thread properly in our main document so the team can review and post.",
    tools=[docs_tool],
    verbose=True,
    llm=llm
)

# === Tasks ===
scrape_task = Task(
    description="Search the web for 3-5 trending tech topics today (e.g. AI, OpenAI, Langchain, startups, LLMs, etc.)",
    expected_output="A bullet list of 3-5 short trend items with 1-line explanation and link",
    agent=trend_scraper
)

summarize_task = Task(
    description="Summarize the collected trends into concise, tweet-style bullets that can be used in social media posts.",
    expected_output="A refined list of 3-5 bullet points under 280 characters each",
    agent=trend_summarizer,
    context=[scrape_task]
)

write_task = Task(
    description=(
        "Write a 2-tweet Twitter thread labeled as 'Tweet 1:' and 'Tweet 2:'. "
        "Start with a hook tweet and follow up with value-add tweet(s). "
        "Avoid using 1/2 or 2/2 format. Also avoid flag emojis like 🇪🇺 — use (EU) instead."
    ),
    expected_output="A 2-tweet formatted thread for Twitter labeled 'Tweet 1:' and 'Tweet 2:'",
    agent=thread_writer,
    context=[summarize_task]
)


thread_save_to_docs = Task(
    description="Save the tweet thread into our fixed Google Docs archive with today's date and timestamp",
    expected_output="Confirmation message with Google Docs URL showing the thread was saved successfully",
    agent=thread_publisher,
    context=[write_task]
)

# === Crew ===
bytebrief_crew = Crew(
    agents=[trend_scraper, trend_summarizer, thread_writer, thread_publisher],
    tasks=[scrape_task, summarize_task, write_task, thread_save_to_docs],
    verbose=True
)

# === Run the crew ===
if __name__ == "__main__":
    print("🚀 Starting ByteBrief Crew...")
    print("="*60)
    
    try:
        result = bytebrief_crew.kickoff()
        print("\n" + "="*60)
        print("✅ FINAL RESULT:")
        print("="*60)
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error running ByteBrief crew: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure you have credentials.json in your project folder")
        print("2. Check your internet connection")
        print("3. Verify your API keys in .env file")