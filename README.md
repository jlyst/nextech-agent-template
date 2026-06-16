# Nextech Catapult AI Session: Experimenting with LLMs for Content Creation

There are a few files in this project that demonstrate ways to use python for LLM inference. Below is a brief overview of the key files:

- `agents.py`: This file defines a multi-agent workflow to research a topic, write an article, and generate a voice script in the `output` folder.

- `tts.py`: This file demonstrates text-to-speech. It reads a script from `output/script.md`, sends it to the TTS endpoint, and saves the resulting audio as a WAV file.

- `demo.py`: This is the file we used to demystify LLMs a bit. It demonstrates how an LLM predicts likely next tokens given an input prompt.