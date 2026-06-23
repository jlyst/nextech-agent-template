import math
import os

from dotenv import load_dotenv
from agno.models.openrouter import OpenRouter

# input = "Respond with only one word and fill in the blank: 'The capital of France is _____.'"
# input = "Continue the opening sentence of a short story that starts with 'The red '. Just continue the sentence and without the first words 'The red '."
input = "Write an opening sentence to an article on one of the top 5 musicians of all time, and begin the sentence with the musician's name."


def main() -> None:
    load_dotenv(".env")
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Add it to .env")

    model = OpenRouter(
        api_key=api_key,
    )

    client = model.get_client()
    response = client.responses.create(
        model="openai/gpt-4.1-mini",
        input=input,
        temperature=1.0,
        max_output_tokens=32,
        top_logprobs=15,
    )
    content = response.output[0].content[0]

    if not content.logprobs:
        print("No token probabilities returned by this model/provider.")
        return

    top_candidates = content.logprobs[0].top_logprobs
    print("\nTop probable next tokens:")
    for candidate in top_candidates:
        probability = math.exp(candidate.logprob)
        print(f"- {candidate.token!r}: {probability:.4f}")

    print(f"\nGenerated text: {content.text!r}\n")


if __name__ == "__main__":
    main()
