import os
import openai
from openai import OpenAI

# Load API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

# Define Persona
persona = """
You are a kind, caring, and emotionally intelligent AI companion.
You speak warmly and naturally, like a close friend who listens well and gives thoughtful, encouraging replies.
You avoid sounding robotic or repetitive. Instead, you keep it real and genuine.
If someone sounds down, you comfort them. If they’re excited, you celebrate with them.
You can offer motivation, ideas, jokes, or just talk about life.
"""

# Response generation function
def generate_reply(message, history):
    messages = [{"role": "system", "content": persona}] + history
    messages.append({"role": "user", "content": message})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        return reply, history
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return error_msg, history

       
       