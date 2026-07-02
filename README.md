# Nextech Catapult AI Session: Experimenting with LLMs for Content Creation

The `agent-team.py` provides a quick introduction on how to create a team of agents for content creation. All outputs are saved in the `output` folder with a timestamp in the filename.

The script does the following:
* defines a team of agents that can 
    * research trending AI stories
    * retrieve stock prices
    * write a markdown article to the output folder
    * write a script for audio narration to the output folder
* generate a voice audio file from the script to the output folder.
* generate an HTML page to the output folder that displays the article with an audio player for the narration.

After running the script, you can open the generated HTML file in a browser to view the article and listen to the audio narration. **You may copy two files 1) the HTML file and 2) the matching audio file (.wav) to a web server to share it with others.**

> The agents use a DeepSeek model from OpenRouter to perform their tasks.


## Running the Script

Run the script with `uv run agent-team.py`. For example,

```terminal
uv run agent-team.py
```

**Make sure to set up your environment variable `OPENROUTER_API_KEY` in a `.env` file before running the code.** We will do this in person.

If you have trouble with the deepseek model, you can switch to the OpenAI GPT-4.1-mini model by uncommenting the lines in the code that use it instead of the deepseek model. Use `"openai/gpt-4.1-mini"` as the model ID.