import os
from dotenv import load_dotenv
from agno.models.openrouter import OpenRouter
from agno.agent import Agent
from agno.workflow import Workflow
from agno.tools.website import WebsiteTools

load_dotenv(".env")

researcher = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Researcher",
    instructions="Select two articles that align with the topic at https://www.therundown.ai. Use the links for the articles to summarize each of the two articles and include relevant embedded links.",
    tools=[WebsiteTools()],
)

article_writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Writer",
    instructions="Write a clear, engaging text-based article based on the research in well-formatted markdown.",
    save_response_to_file="output/news.md",
)

script_writer = Agent(
    model=OpenRouter(id="deepseek/deepseek-v4-flash"),
    name="Script Writer",
    instructions="Write a clear, engaging voice script based on the article in well-formatted markdown that will be used to generate audio content directly. All text will be converted to speech, so avoid including any markdown formatting or special characters that are not meant to be read aloud.",
    save_response_to_file="output/script.md",
)

content_workflow = Workflow(
    name="Content Creation",
    steps=[researcher, article_writer, script_writer],
)

content_workflow.print_response("Write an article about AI trends", stream=True)
