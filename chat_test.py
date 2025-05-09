import os
from openai import OpenAI

def get_chatgpt(): #This function will get a ChatGPT response.
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Obtain the API key from the environment variable.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "hello"}] ,# Set the prompt.
        max_tokens= 30 # Limit the maximum number of tokens in a response.
    )
    print(response.choices[0].message.content)
if __name__ == "__main__":
    get_chatgpt()
