import os
import openai
import tempfile
from gtts import gTTS
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
        return reply, history
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return error_msg, history

# Voice chat logic
def voice_chat(audio, history):
    if audio is None:
        return "Please say something.", None, history

    # Transcription
    text_input = audio  # Gradio auto-converts to text if `type="filepath"`
    reply, history = respond(text_input, history)

    # TTS
    tts = gTTS(text=reply, lang="en")
    tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tts_file.name)

    return reply, tts_file.name, history

# Launch Gradio App
def launch_app():
    mode = gr.State("dark")
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

    with gr.Blocks() as demo:
        state = gr.State([])

        gr.Markdown("<h1 style='text-align:center; color:#3b82f6;'>SearchBot 🔍</h1><p style='text-align:center;'>Speak or type to your AI companion</p>")

        css_selector = gr.HTML("<style id='custom-theme'></style>")
        js_toggle = gr.Button("🌗 Toggle Theme")

        chatbot = gr.Chatbot(elem_id="chatbot", type="messages", avatar_images=("🧑", "🤖"))
        msg = gr.Textbox(placeholder="Type here...", show_label=False)
        voice_input = gr.Audio(source="microphone", type="filepath", label="🎤 Voice Input")
        voice_output = gr.Audio(label="🔊 Bot Voice", autoplay=True)
        send_btn = gr.Button("Send Voice")

        # Text input response
        msg.submit(fn=lambda m, h: respond(m, h), inputs=[msg, state], outputs=[chatbot, state])

        # Voice chat handler
        send_btn.click(fn=voice_chat, inputs=[voice_input, state], outputs=[chatbot, voice_output, state])

        # Theme toggle handler
        def toggle_theme(current_mode):
            return (
                gr.update(value="light") if current_mode == "dark" else gr.update(value="dark"),
                f"<style>{light_css if current_mode == 'dark' else dark_css}</style>"
            )

        js_toggle.click(toggle_theme, [mode], [mode, css_selector])
        css_selector.value = f"<style>{dark_css}</style>"

    demo.launch()

if __name__ == "__main__":
    launch_app()
