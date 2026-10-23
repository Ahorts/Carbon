import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Carbon agent")
parser.add_argument("user_prompt", type=str, help="Enter a message to send to the AI agent")
parser.add_argument("--verbose", action="store_true", help="enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "user", "content": args.user_prompt}
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    
)

if response.usage is None:
    raise RuntimeError("Request failed")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
print(response.choices[0].message.content)

