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

timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M")

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
    role="Write a well-formatted markdown of the findings.",
    save_response_to_file=f"output/{timestamp}_article.md",
)

script_writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Script Writer",
    role="Write a script for the audio narration of the findings. Output only the script text that will be read without any additional commentary or instructions.",
    save_response_to_file=f"output/{timestamp}_script.txt",
)

team_coordinator = Team(
    name="Research Team",
    members=[news_agent, finance_agent, article_writer, script_writer],
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    instructions="Delegate to the appropriate agent based on the request.",
)

team_coordinator.print_response(
    "What are the top 3 trending AI stories and how is NVDA stock doing? Write an article and a script for the audio narration of the findings.",
    stream=True,
)

# Convert the output to speech
script_file = f"output/{timestamp}_script.txt"
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

    with wave.open(f"output/{timestamp}_audio.wav", "wb") as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(24000)  # 24 kHz
        wf.writeframes(response.content)

    print(
        f"Audio saved to output/{timestamp}_audio.wav. Generation ID: {response.headers.get('X-Generation-Id')}"
    )

# Generate HTML page with article and optional audio widget
article_file = f"output/{timestamp}_article.md"
audio_file = f"output/{timestamp}_audio.wav"
html_file = f"output/{timestamp}_article.html"

with open(article_file, "r") as f:
    article_md = f.read()

audio_widget = ""
if os.path.exists(audio_file):
    audio_widget = f'<audio controls style="width:100%;margin-bottom:2rem"><source src="{timestamp}_audio.wav" type="audio/wav"></audio>'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Research Report {timestamp}</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{ max-width: 800px; margin: 2rem auto; padding: 0 1rem; font-family: sans-serif; }}
  </style>
</head>
<body>
  {audio_widget}
  <div id="content"></div>
  <script>
    document.getElementById("content").innerHTML = marked.parse({repr(article_md)});
  </script>
</body>
</html>"""

with open(html_file, "w") as f:
    f.write(html)

print(f"HTML report saved to {html_file}")
