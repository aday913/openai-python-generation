import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate Python script from a prompt using OpenAI API.")
    parser.add_argument('prompt', help="The prompt or path to a .txt file containing the prompt", nargs='?')
    args = parser.parse_args()

    load_dotenv()

    # Check if prompt is provided
    if not args.prompt:
        print("Please provide a prompt or a path to a .txt file containing the prompt.")
        sys.exit(1)

    # Check if the prompt is a file path
    try:
        with open(args.prompt, 'r') as file:
            prompt = file.read()
    except FileNotFoundError:
        prompt = args.prompt

    # Configure OpenAI API key
    client = OpenAI(
        api_key=f"{os.getenv('APIKEY')}",
    )

    # Send prompt to OpenAI API
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'Responding only with the code needed and with no other text, please provide me a python script for the following prompt: {prompt}',
                }
            ],
            model="gpt-3.5-turbo",
        )
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        sys.exit(1)

    # Save the response to a file
    with open('generated_script.py', 'w') as file:
        print(f'Generated response:')
        print(f'{chat_completion.choices[0].message.content.strip()}')
        file.write(chat_completion.choices[0].message.content.strip())

    print("Generated script saved as 'generated_script.py'.")

if __name__ == "__main__":
    main()