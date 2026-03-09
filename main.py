import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

MODEL = "gemini-2.5-flash-lite"


def get_args(desc="Default"):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def return_verbose(response, args):
    metadata = response.usage_metadata
    if not metadata:
        raise RuntimeError("The model didn't wield a response")
    return (
        "\n".join(
            [
                "====================================================",
                f"User prompt: {args.user_prompt}",
                f"Prompt tokens: {metadata.prompt_token_count}",
                f"Response tokens: {metadata.candidates_token_count}",
            ]
        )
        + f"\n{return_normal(response, True)}\n===================================================="
    )


def return_normal(response, verbose_function=False):
    ret = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(
                function_call, True if verbose_function else False
            )
            if not function_call_result.parts:
                raise Exception(
                    f"function call {function_call.name} result did not return parts"
                )
            function_response = function_call_result.parts[0].function_response
            if not function_response:
                raise Exception(
                    f"function call {function_call.name} did not yield a response"
                )
            if not function_response.response:
                raise Exception(
                    f"The response field for {function_call.name} is missing!"
                )
            if verbose_function:
                ret.append(f"-> {function_response.response}")
    else:
        ret.append(f"Response: {response.text}")
    return "\n".join(ret)


def request_response(client):
    args = get_args()
    prompt = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    return return_verbose(response, args) if args.verbose else return_normal(response)


def main():
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError(
            "The API Key was not found. Please ensure that you have a .env with your Google AI key"
        )
    try:
        client = genai.Client(api_key=api_key)
        print(request_response(client))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
