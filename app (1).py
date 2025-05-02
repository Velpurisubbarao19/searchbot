import os
import openai
import gradio as gr

from openai import OpenAI

# Load API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

# Persona
persona = """
You are a kind, caring, and emotionally intelligent AI companion.
You speak warmly and naturally, like a close friend who listens well and gives thoughtful, encouraging replies.
You avoid sounding robotic or repetitive. Instead, you keep it real and genuine.
If someone sounds down, you comfort them. If they’re excited, you celebrate with them.
You can offer motivation, ideas, jokes, or just talk about life.
"""

# Chat logic
def respond(message, history):
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
        return history, history
    except Exception as e:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        return history, history

# UI Setup
with gr.Blocks() as demo:
    mode = gr.State("dark")  # Default theme mode

    dark_css = """
        body { background-color: #0a192f; color: #dbeafe; font-family: 'Segoe UI', sans-serif; }
        #chatbot { background-color: #112240; border-radius: 16px; padding: 20px; }
        .message.user { background-color: #1e293b !important; color: #e0f2fe; }
        .message.bot { background-color: #1e40af !important; color: #f1f5f9; }
        textarea { background-color: #1e293b !important; color: #f8fafc; border: 1px solid #3b82f6; }
    """
    light_css = """
        body { background-color: #f1f5f9; color: #1e293b; font-family: 'Segoe UI', sans-serif; }
        #chatbot { background-color: #ffffff; border-radius: 16px; padding: 20px; }
        .message.user { background-color: #e2e8f0 !important; color: #1e293b; }
        .message.bot { background-color: #3b82f6 !important; color: #ffffff; }
        textarea { background-color: #ffffff !important; color: #1e293b; border: 1px solid #3b82f6; }
    """

    css_selector = gr.HTML("<style id='custom-theme'></style>")
    js_toggle = gr.Button("🌗 Toggle Theme")
    
    gr.Markdown("""
        <div style="text-align: center;">
            <h1 style="color: #3b82f6;">SearchBot 🔍</h1>
            <p>Your thoughtful, curious, and friendly AI companion.</p>
        </div>
    """)

    chatbot = gr.Chatbot(elem_id="chatbot", type="messages", avatar_images=("🧑", "🤖"))
    msg = gr.Textbox(placeholder="Ask me anything...", show_label=False)
    state = gr.State([])

    msg.submit(respond, [msg, state], [chatbot, state])

    # JS to inject theme dynamically
    def toggle_theme(current_mode):
        if current_mode == "dark":
            return gr.update(value="light"), f"<style>{light_css}</style>"
        else:
            return gr.update(value="dark"), f"<style>{dark_css}</style>"

    js_toggle.click(toggle_theme, [mode], [mode, css_selector])

    # Set initial theme
    css_selector.value = f"<style>{dark_css}</style>"

demo.launch()

