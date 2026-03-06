import os
import argparse
from dotenv import load_dotenv
from google import genai


def get_args(desc="Default"):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("user_prompt", type=str, help="User prompt")
    return parser.parse_args()


def generate_response(client):
    prompt = get_args().user_prompt
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model=model, contents=prompt)
    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("The model didn't wield a response")
    answer_msg = [
        f"User Prompt: {prompt}",
        f"Prompt tokens: {metadata.prompt_token_count}",
        f"Response tokens: {metadata.candidates_token_count}",
        f"Response: {response.text}",
    ]
    return "\n".join(answer_msg)


def main():
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError(
            "The API Key was not found. Please ensure that you have a .env with your Google AI key"
        )
    client = genai.Client(api_key=api_key)
    print(generate_response(client))


if __name__ == "__main__":
    main()
