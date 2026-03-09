import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

MODEL = "gemini-2.5-flash"


def get_args(desc="Default"):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def return_verbose(response):
    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("The model didn't wield a response")
    return "\n".join(
        [
            "====================================================",
            f"User prompt: {get_args().user_prompt}",
            f"Prompt tokens: {metadata.prompt_token_count}",
            f"Response tokens: {metadata.candidates_token_count}",
            f"{return_normal(response)}",
            "====================================================",
        ]
    )


def return_normal(response):
    ret = []
    if response.function_calls:
        for function_call in response.function_calls:
            ret.append(f"Calling function: {function_call.name}({function_call.args})")
    else:
        ret.append(f"Response: {response.text}")
    return "\n".join(ret)


def request_response(client):
    prompt = get_args().user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    return return_verbose(response) if get_args().verbose else return_normal(response)


def main():
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError(
            "The API Key was not found. Please ensure that you have a .env with your Google AI key"
        )
    client = genai.Client(api_key=api_key)
    print(request_response(client))


if __name__ == "__main__":
    main()
