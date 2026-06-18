# Nextech Catapult AI Session: Experimenting with LLMs for Content Creation

There are a few files in this project that demonstrate ways to use python for LLM inference. Below is a brief overview of the key files:

- `agent-workflow.py`: This file defines a multi-agent workflow to research a topic, write an article, and generate a voice script in the `output` folder.

- `agent-team.py`: This file defines a team of agents that can be used to research trending AI stories and stock prices, and write a markdown file summarizing the findings.

- `tts.py`: This file demonstrates text-to-speech. It reads a script from `output/script.md`, sends it to the TTS endpoint, and saves the resulting audio as a WAV file.

- `demo.py`: This is the file we used to demystify LLMs a bit. It demonstrates how an LLM predicts likely next tokens given an input prompt.

## Running Scripts

Run each file with `uv run <file_name>`. For example,

```terminal
uv run demo.py
```

**Make sure to set up your environment variable `OPENROUTER_API_KEY` in a `.env` file before running the code.**