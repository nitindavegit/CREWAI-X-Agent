from dotenv import load_dotenv
load_dotenv()

import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from google_docs_tool import GoogleDocsTool

# Setup Gemini LLM 
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.3
)

# Tools 
search_tool = SerperDevTool()
docs_tool = GoogleDocsTool()

# Check if Google Docs is properly configured
if not os.path.exists('credentials.json'):
    print("⚠️  WARNING: credentials.json not found!")
    print(docs_tool.get_setup_instructions())
    print("\n" + "="*60)

# Enhanced Agents with Personalities with better prompts 
trend_scraper = Agent(
    role="Elite Tech Intelligence Analyst",
    goal="Discover 3-5 high-impact, trending tech stories from the last 24 hours that will generate maximum social media engagement",
    backstory="""You are a seasoned tech journalist with 10+ years of experience spotting viral tech stories. 
    You have an exceptional ability to identify stories that developers and tech enthusiasts will share, comment on, and engage with.
    You prioritize breaking news, major product launches, significant funding rounds, controversial decisions by tech giants, 
    and emerging technologies that are gaining momentum. You always verify source credibility and prefer primary sources over aggregators.""",
    verbose=True,
    tools=[search_tool],
    llm=llm,
    max_execution_time=120,
    allow_delegation=False
)

trend_analyzer = Agent(
    role="Viral Content Strategist",
    goal="Transform raw tech news into share-worthy insights that maximize social media impressions and engagement",
    backstory="""You are a social media strategist specializing in tech content who understands exactly what makes content go viral.
    You analyze trending topics not just for what happened, but for WHY it matters to the tech community.
    You identify the human impact, future implications, and controversial angles that spark discussion.
    You always consider: 'What would make a developer stop scrolling and share this?'""",
    verbose=True,
    llm=llm,
    max_execution_time=90
)

viral_thread_creator = Agent(
    role="X (Twitter) Growth Specialist",
    goal="Craft 2-tweet threads optimized for maximum impressions, retweets, and engagement using trending hashtags and viral techniques",
    backstory="""You are a Twitter growth expert who has helped accounts grow from zero to 100K+ followers.
    You understand Twitter's algorithm deeply and know exactly how to structure content for maximum reach.
    You craft hooks that stop the scroll, use TRENDING hashtags (not generic ones), and create content people WANT to share.
    
    You never use '🚨 BREAKING:' style alerts, but you master other engagement techniques like questions, 
    surprising facts, future predictions, and 'what this means for you' angles. 
    
    HASHTAG STRATEGY: You always research and use hashtags that are currently trending on Twitter related to the topic.
    For example: If the story is about OpenAI, you use #OpenAI #ChatGPT #GPT if they're trending, not generic #AI #Tech.
    You balance trending hashtags with evergreen ones based on tweet length.""",
    verbose=True,
    tools=[search_tool],
    llm=llm,
    max_execution_time=120
)

archive_manager = Agent(
    role="Content Archive Specialist",
    goal="Professionally document and organize tweet threads in Google Docs with proper formatting and metadata",
    backstory="""You are a meticulous content manager who ensures every piece of content is properly archived
    for future reference and analysis. You understand the importance of clean documentation for content strategy
    and always confirm successful saves with professional status updates.""",
    tools=[docs_tool],
    verbose=True,
    llm=llm,
    max_execution_time=60
)

# Enhanced Tasks with better prompts
intelligence_gathering = Task(
    description="""Search for 3-5 trending tech stories from the last 24 hours that have viral potential.
    
    Focus on:
    - Breaking news from major tech companies (OpenAI, Google, Microsoft, Apple, Meta, etc.)
    - Significant product launches or updates
    - Major funding rounds or acquisitions
    - Controversial decisions or industry shifts
    - Emerging technologies gaining traction
    - Developer tools or platform changes
    
    For each story, verify:
    - Source credibility (prefer official announcements, TechCrunch, Ars Technica, The Verge, etc.)
    - Recency (within 24 hours)
    - Engagement potential (comments, discussions, controversy level)
    
    Search queries to try: "latest tech news today", "AI news today", "startup funding today", "developer tools", "tech companies news"
    """,
    expected_output="""A curated list of 3-5 trending tech stories with:
    - Story headline and brief description
    - Why it's trending/viral-worthy
    - Source credibility rating
    - Potential engagement angle
    - URL to primary source
    
    Format: 
    1. [STORY TITLE] - [1-2 sentence description] 
       Source: [credible source] | Viral Factor: [why it will get shares/engagement]
       Link: [URL]""",
    agent=trend_scraper
)

viral_analysis = Task(
    description="""Analyze the discovered trends and identify the single most share-worthy story for maximum social media impact.
    
    Consider:
    - Which story would developers/tech enthusiasts most likely share?
    - What angle or insight would spark discussion?
    - What's the broader implication that people care about?
    - How can this be positioned to maximize engagement?
    
    Select the ONE best story and develop the viral angle.""",
    expected_output="""The selected top story with:
    - Chosen story and rationale for selection
    - Viral angle/hook (what makes it shareable)
    - Key talking points that spark engagement
    - Target audience appeal (why developers/tech people care)
    - Engagement prediction (likes, retweets, comments potential)""",
    agent=trend_analyzer,
    context=[intelligence_gathering]
)

thread_creation = Task(
    description="""Create a 2-tweet Twitter thread optimized for maximum impressions and engagement using TRENDING hashtags.
    
    PHASE 1 - TRENDING HASHTAG RESEARCH:
    First, search for what hashtags are currently trending related to your story topic.
    Search queries like: "[topic] trending hashtags Twitter", "Twitter trends [company/topic]", "#[maintopic] trending"
    
    PHASE 2 - THREAD CREATION:
    Requirements:
    - Format: "Tweet 1:" and "Tweet 2:" labels
    - NO "🚨 BREAKING:" or similar alert styles
    - Tweet 1: Hook that stops the scroll (question, surprising fact, bold prediction, or "what this means")
    - Tweet 2: Value-add with actionable insights or future implications
    
    HASHTAG STRATEGY (CRITICAL FOR MAXIMUM IMPRESSIONS):
    - Use TRENDING hashtags related to your topic (e.g., if OpenAI story, use #OpenAI #ChatGPT #GPT4 if trending)
    - Mix trending + 1-2 evergreen tech hashtags (#AI #Tech #Developer)
    - Fewer hashtags if tweet is long, more if short (max 280 chars per tweet)
    - Research what's actually trending on Twitter today, don't guess
    
    Hook styles to use:
    - Questions: "What if..." "Did you know..." "Why are..."
    - Numbers: "3 reasons why..." "The $X billion impact of..."  
    - Predictions: "This changes everything for..." "The future of X just shifted..."
    - Impact: "What this means for developers..." "Why every startup should care..."
    
    Optimize for virality AND trending hashtag visibility.""",
    expected_output="""A perfectly formatted 2-tweet thread with trending hashtags:
    
    Tweet 1: [Engaging hook under 280 chars with TRENDING + strategic hashtags]
    
    Tweet 2: [Value-add content under 280 chars with TRENDING + strategic hashtags]""",
    agent=viral_thread_creator,
    context=[viral_analysis]
)

archive_thread = Task(
    description="""Save the completed tweet thread to Google Docs with proper formatting and metadata.
    
    Include:
    - Current date and timestamp
    - The complete thread content
    - Source story reference
    - Engagement predictions
    - Clean, professional formatting
    
    Confirm successful save with Google Docs URL.""",
    expected_output="""Professional confirmation message:
    ✅ Tweet thread successfully archived to Google Docs
    📊 Content: [brief description of thread topic]
    📅 Date: [current date/time]  
    🔗 Archive URL: [Google Docs link]
    📈 Predicted engagement: [engagement metrics from thread creation]""",
    agent=archive_manager,
    context=[thread_creation]
)

# === Enhanced Crew Configuration ===
bytebrief_crew = Crew(
    agents=[trend_scraper, trend_analyzer, viral_thread_creator, archive_manager],
    tasks=[intelligence_gathering, viral_analysis, thread_creation, archive_thread],
    verbose=True,
    max_execution_time=600
)

# Enhanced Execution with Better Error Handling 
if __name__ == "__main__":
    print("🚀 Starting Enhanced ByteBrief Crew...")
    print("📊 Mission: Create viral tech content for maximum X impressions")
    print("🎯 Target: Developers & tech enthusiasts")
    print("⏱️  Timeline: Last 24 hours trending content")
    print("="*70)
    
    try:
        print("\n🔍 Phase 1: Intelligence Gathering...")
        print("🧠 Phase 2: Viral Content Analysis...")
        print("✍️  Phase 3: Thread Creation...")
        print("💾 Phase 4: Archive Management...")
        print("\n" + "="*70)
        
        result = bytebrief_crew.kickoff()
        
        print("\n" + "="*70)
        print("✅ BYTEBRIEF MISSION COMPLETE!")
        print("="*70)
        print(result)
        print("\n🎉 Ready to post and grow your X following!")
        
    except Exception as e:
        print(f"\n❌ ByteBrief Mission Failed: {str(e)}")
        print("\n🔧 Troubleshooting Checklist:")
        print("   ☐ credentials.json exists in project folder")
        print("   ☐ Internet connection stable")  
        print("   ☐ API keys properly configured in .env")
        print("   ☐ Google Docs API enabled in Google Cloud Console")
        print("\n💡 This is a demo-friendly error for showcasing real-world reliability!")