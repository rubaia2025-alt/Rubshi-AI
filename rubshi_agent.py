"""
Rubshi AI Agent - Pink Paradise Edition
Gradio 6 compatible
Chalano: python rubshi_agent.py
"""

import os
from getpass import getpass

import gradio as gr
from google import genai

print("=" * 50)
print("  Rubshi AI Agent shuru hocche...")
print("=" * 50)

api_key = os.environ.get("GEMINI_API_KEY") or getpass(
    "Tomar Gemini API key paste koro (typing dekhabe na): "
).strip()

if not api_key:
    raise SystemExit("API key nei. Abar run koro ar key dao.")

client = genai.Client(api_key=api_key)

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest",
]

SYSTEM_PROMPT = """Tumi "Rubshi" - ekta friendly, cute, smart personal AI assistant.

Rules:
- User jei bhashay likhbe, tumi sei bhashay uttor dibe. Bangla hole shohoj Bangla.
- Friendly, warm, helpful tone e kotha bolo. Majhe majhe emoji use koro.
- Short, clear uttor dao. Proyojon na thakle lamba lekho na.
- Jodi sure na hou, shotti kotha bolo - bhul information diye na.
- Code chaile clean, comment-shoho code dao.
"""


def build_prompt(message, history):
    """History + notun message theke full prompt banao."""
    parts = [SYSTEM_PROMPT, "", "Conversation so far:"]

    recent_history = (history or [])[-4:]
    for item in recent_history:
        if isinstance(item, dict):
            role = item.get("role", "")
            content = item.get("content", "")
            if isinstance(content, list):
                content = " ".join(
                    p.get("text", "") for p in content if isinstance(p, dict)
                )
            content = str(content).strip()
            if role == "user" and content:
                parts.append(f"User: {content}")
            elif role == "assistant" and content:
                parts.append(f"Rubshi: {content}")

    parts.append(f"User: {message.strip()}")
    parts.append("Rubshi:")
    return "\n".join(parts)


def chat(message, history):
    message = (message or "").strip()
    if not message:
        yield "Kichu likho, tarpor pathao"
        return

    prompt = build_prompt(message, history)

    for model in MODELS:
        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=prompt,
            )
            full_text = ""
            for chunk in stream:
                if getattr(chunk, "text", None):
                    full_text += chunk.text
                    yield full_text
            if full_text.strip():
                print(f"[OK] uttor dilo: {model}")
                return
        except Exception as e:
            print(f"[FAIL] {model}: {type(e).__name__}: {e}")
            continue

    yield "Dukkhito, ekhon uttor dite parchi na. Terminal er error dekho."


# ---------- Custom CSS - Pink Paradise with Background Image ----------
CUSTOM_CSS = """
.gradio-container {
    background-image: url('/file=C:/Users/UESR/Downloads/background.jpg') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
    min-height: 100vh !important;
}

body {
    background: linear-gradient(135deg, #ffd1dc 0%, #ffb6c1 50%, #ffc0cb 100%) !important;
}

.gradio-container h1 {
    text-align: center !important;
    color: #ffffff !important;
    text-shadow: 0 0 25px rgba(255, 105, 180, 1), 2px 2px 10px rgba(0, 0, 0, 0.4) !important;
    font-size: 2.5em !important;
    font-weight: 800 !important;
}

.gradio-container h3 {
    text-align: center !important;
    color: #ffffff !important;
    text-shadow: 1px 1px 8px rgba(0, 0, 0, 0.5) !important;
}

#rubshi-chat {
    border-radius: 24px !important;
    box-shadow: 0 15px 40px rgba(255, 105, 180, 0.4) !important;
    border: 2px solid rgba(255, 255, 255, 0.6) !important;
    background: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}

#rubshi-input textarea {
    border-radius: 16px !important;
    border: 2px solid rgba(255, 182, 193, 0.9) !important;
    padding: 14px 18px !important;
    font-size: 1em !important;
    background: rgba(255, 255, 255, 0.95) !important;
    color: #4a1a2c !important;
}

#rubshi-input textarea:focus {
    border-color: #ff69b4 !important;
    box-shadow: 0 0 0 4px rgba(255, 105, 180, 0.3) !important;
}

#rubshi-input button {
    border-radius: 16px !important;
    background: linear-gradient(135deg, #ff69b4, #ff1493) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5) !important;
}

.examples button, .example {
    border-radius: 20px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border: 2px solid rgba(255, 105, 180, 0.6) !important;
    color: #c2185b !important;
    font-weight: 500 !important;
}

footer { display: none !important; }
"""


# ---------- UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# Rubshi AI")
    gr.Markdown("### Tomar cute personal AI assistant")

    chatbot = gr.Chatbot(
        elem_id="rubshi-chat",
        height=480,
        show_label=False,
    )

    gr.ChatInterface(
        fn=chat,
        chatbot=chatbot,
        textbox=gr.Textbox(
            elem_id="rubshi-input",
            placeholder="Ekhane tomar proshno likho...",
            container=False,
            scale=7,
        ),
        examples=[
            "Tomar nam ki? Banglay bolo.",
            "Python e Fibonacci code likhe dao.",
            "Ekta AI agent ki? Simple kore bujhao.",
        ],
    )


if __name__ == "__main__":
    print("\nRubshi ready! Terminal e URL ashbe, seta browser e kholo.\n")
    demo.launch(css=CUSTOM_CSS)