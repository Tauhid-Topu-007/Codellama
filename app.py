import json
import socket
import requests
import gradio as gr

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "coder"


def find_free_port():
    """Ask the OS for any free port (avoids Windows reserved ranges)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def to_text(content):
    """Gradio versions differ: content may be a string or a list of blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            c.get("text", "") if isinstance(c, dict) else str(c) for c in content
        )
    return str(content)


def build_messages(message, history, system_prompt):
    msgs = []
    if system_prompt.strip():
        msgs.append({"role": "system", "content": system_prompt})
    for item in history:
        if isinstance(item, dict):  # messages format
            msgs.append({"role": item["role"], "content": to_text(item["content"])})
        else:  # old tuple format
            user, bot = item
            if user:
                msgs.append({"role": "user", "content": to_text(user)})
            if bot:
                msgs.append({"role": "assistant", "content": to_text(bot)})
    msgs.append({"role": "user", "content": to_text(message)})
    return msgs


def chat(message, history, model, system_prompt, temperature):
    payload = {
        "model": model,
        "messages": build_messages(message, history, system_prompt),
        "stream": True,
        "options": {"temperature": temperature},
    }
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=600) as r:
            if r.status_code != 200:
                yield f"⚠️ Error {r.status_code}: {r.text}"
                return
            partial = ""
            for line in r.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                partial += chunk.get("message", {}).get("content", "")
                yield partial
                if chunk.get("done"):
                    break
    except requests.exceptions.ConnectionError:
        yield "⚠️ Can't reach Ollama. Make sure it's running (`ollama serve`)."


demo = gr.ChatInterface(
    fn=chat,
    title="💻 Code Assistant",
    description="Local coding assistant powered by Ollama.",
    additional_inputs=[
        gr.Textbox(value=DEFAULT_MODEL, label="Model name"),
        gr.Textbox(
            value="You are an expert programming assistant. Give clear, correct code with brief explanations.",
            label="System prompt",
            lines=3,
        ),
        gr.Slider(0.0, 1.5, value=0.2, step=0.05, label="Temperature"),
    ],
    additional_inputs_accordion=gr.Accordion("⚙️ Settings", open=False),
    examples=[
        ["Write a Python function to reverse a linked list", DEFAULT_MODEL,
         "You are an expert programming assistant.", 0.2],
        ["Explain async/await in JavaScript with an example", DEFAULT_MODEL,
         "You are an expert programming assistant.", 0.2],
    ],
)

if __name__ == "__main__":
    port = find_free_port()
    print(f"Starting on http://127.0.0.1:{port}")
    demo.launch(server_name="127.0.0.1", server_port=port)