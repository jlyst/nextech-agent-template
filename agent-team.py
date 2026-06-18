import os
from dotenv import load_dotenv
from agno.team import Team
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools

load_dotenv(".env")

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

writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Writer",
    instructions="Write a well-formatted markdown of the findings.",
    save_response_to_file="output/updates.md",
)

team = Team(
    name="Research Team",
    members=[news_agent, finance_agent, writer],
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    instructions="Delegate to the appropriate agent based on the request.",
)

team.print_response(
    "What are the trending AI stories and how is NVDA stock doing? Write a well-formatted markdown file of the findings.",
    stream=True,
)
