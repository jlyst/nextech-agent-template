import os
import wave
import requests
from datetime import datetime
from dotenv import load_dotenv
from agno.team import Team
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools

load_dotenv(".env")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

news_agent = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="News Agent",
    role="Get trending tech news from HackerNews",
    tools=[HackerNewsTools()],
)

finance_agent = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Finance Agent",
    role="Get stock prices and financial data",
    tools=[YFinanceTools()],
)

article_writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Writer",
    instructions="Write a well-formatted markdown of the findings.",
    save_response_to_file=f"output/article_{timestamp}.md",
)

script_writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Script Writer",
    instructions="Write a script for the audio narration of the findings. Output only the script text without any additional commentary.",
    save_response_to_file=f"output/script_{timestamp}.txt",
)

team = Team(
    name="Research Team",
    members=[news_agent, finance_agent, article_writer, script_writer],
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    instructions="Delegate to the appropriate agent based on the request.",
)

team.print_response(
    "What are the top 3 trending AI stories and how is NVDA stock doing? Write an article and a script for the audio narration of the findings.",
    stream=True,
)

# Convert the output to speech
script_file = f"output/script_{timestamp}.txt"
if not os.path.exists(script_file):
    print(f"No {script_file} found, skipping TTS.")
else:
    with open(script_file, "r") as f:
        script_text = f.read()

    response = requests.post(
        url="https://openrouter.ai/api/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "hexgrad/kokoro-82m",
            "input": script_text,
            "voice": "af_heart",
            "speed": 1.5,
        },
    )

    with wave.open(f"output/news_{timestamp}.wav", "wb") as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(24000)  # 24 kHz
        wf.writeframes(response.content)

    print(
        f"Audio saved to output/news_{timestamp}.wav. Generation ID: {response.headers.get('X-Generation-Id')}"
    )
