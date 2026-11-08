# CodeLlama — Local AI Coding Assistant

A lightweight, locally hosted coding assistant built with **Ollama** and **Gradio**. The application provides a ChatGPT-style interface for asking programming questions while sending prompts to a model running on your own machine.

The repository includes a Gradio chat application, an Ollama model configuration, and Python dependencies.

## Features

- **Local model inference:** Connects to the Ollama API at `http://localhost:11434/api/chat`.
- **Interactive chat UI:** Uses Gradio's `ChatInterface` for a browser-based conversation experience.
- **Streaming responses:** Displays generated text progressively as Ollama returns response chunks.
- **Conversation context:** Sends previous user and assistant messages with each new prompt.
- **Configurable model:** Change the Ollama model name in the interface.
- **Custom system prompt:** Set the assistant's role and response instructions.
- **Temperature control:** Adjust response randomness from 0.0 to 1.5.
- **Example prompts:** Includes sample programming questions to help you get started.
- **Local access:** Starts on a free available localhost port and binds to `127.0.0.1`.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Ollama | Local LLM runtime and chat API |
| Code Llama | Code-focused language model |
| Gradio | Web-based chat interface |
| Requests | HTTP communication with Ollama |
| JSON | Streaming response parsing |

## Project Structure

```text
Codellama/
├── app.py           # Gradio chat application and Ollama API integration
├── modelfile        # Ollama model configuration for the "coder" model
├── requirements.txt # Python package requirements
└── README.md
```

## Requirements

- Python 3.9 or newer
- [Ollama](https://ollama.com/) installed and available in your system PATH
- A Code Llama model downloaded through Ollama
- Enough RAM / GPU memory for the model you choose

> **Note:** Model resource requirements vary by model size and quantization. Start with a smaller model if your machine has limited memory.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Tauhid-Topu-007/Codellama.git
cd Codellama
```

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install requests
```

The application imports `gradio` and `requests`. The current requirements file also includes `langchain`, although the present `app.py` does not directly use it.

### 4. Install and start Ollama

Install Ollama from [ollama.com](https://ollama.com/), then start the Ollama service.

In a terminal, verify that Ollama is available:

```bash
ollama --version
```

If Ollama is not already running, start it:

```bash
ollama serve
```

Keep the Ollama service running while using the application.

### 5. Download the Code Llama model

In another terminal:

```bash
ollama pull codellama
```

This downloads the base model referenced by the repository's model configuration. Model download size depends on the Ollama model variant.

### 6. Create the custom model

The included `modelfile` defines a model named `coder` based on `codellama`, with a system instruction and temperature parameter.

Run this command from the repository root:

```bash
ollama create coder -f modelfile
```

You can test the model directly:

```bash
ollama run coder
```

The Gradio application uses `coder` as its default model name.

## Run the Application

Make sure Ollama is running and the `coder` model has been created. Then run:

```bash
python app.py
```

The terminal prints the local URL, for example:

```text
Starting on http://127.0.0.1:7860
```

The actual port is selected dynamically and may be different. Open the URL printed in your terminal in a web browser.

## Using the Chat Interface

1. Enter a programming question in the chat input.
2. Submit the prompt and wait for the model to stream its response.
3. Open **Settings** to customize the model name, system prompt, or temperature.
4. Continue the conversation to ask follow-up questions; previous chat messages are included as context.

### Settings

| Setting | Description |
|---|---|
| Model name | Ollama model tag to send in the API request; defaults to `coder` |
| System prompt | Instructions that define the assistant's behavior |
| Temperature | Controls response randomness; lower values generally produce more focused output |

### Example Prompts

- Write a Python function to reverse a linked list.
- Explain async/await in JavaScript with a practical example.
- Find the time and space complexity of binary search.
- Refactor this code for readability and maintainability.
- Explain this error and suggest a debugging strategy.
- Generate unit tests for the following function.

## How It Works

```text
        User
         |
         v
   Gradio Chat UI
         |
         v
      app.py
         |
         | HTTP POST /api/chat
         | (messages, model, temperature)
         v
   Ollama API Server
         |
         v
   Local Code Llama Model
         |
         | streamed JSON response chunks
         v
      app.py
         |
         | accumulated response text
         v
   Gradio Chat UI
         |
         v
        User
```

1. Gradio calls the `chat()` function when a user submits a message.
2. `build_messages()` combines the optional system prompt, conversation history, and current message.
3. The application sends a streaming request to Ollama's `/api/chat` endpoint.
4. Ollama generates a response using the selected local model.
5. The application reads newline-delimited JSON chunks and yields the accumulated response to Gradio.

## Configuration

The main application settings are defined near the top of `app.py`:

| Variable | Current value | Purpose |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/api/chat` | Ollama chat endpoint |
| `DEFAULT_MODEL` | `coder` | Default model name |

To use another model, pull it with Ollama and enter its exact model tag in the **Model name** setting.

The model behavior is configured in `modelfile`. After editing that file, recreate the model:

```bash
ollama create coder -f modelfile
```

## Troubleshooting

### Can't reach Ollama

The application displays a connection warning when it cannot connect to Ollama.

- Confirm Ollama is installed.
- Start the service with `ollama serve` if it is not running.
- Check that the API is reachable at `http://localhost:11434`.
- Make sure local firewall or proxy settings are not blocking the connection.

### Model not found

If Ollama reports that the model does not exist:

```bash
ollama list
ollama pull codellama
ollama create coder -f modelfile
```

Confirm that the model name in the Gradio settings matches an installed Ollama model.

### Missing Python package

Activate your virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
pip install requests
```

### Slow responses or memory errors

- Try a smaller or more highly quantized Ollama model.
- Close other memory-intensive applications.
- Reduce the complexity of prompts and the amount of conversation history.
- Check Ollama's logs for model-loading or resource errors.

## Security and Privacy

- The application binds the Gradio server to `127.0.0.1`, so it is intended for local use.
- Prompts are sent to the Ollama service configured in `app.py`; with the default local endpoint, inference runs on your machine.
- Do not expose the Gradio interface or Ollama API publicly without adding appropriate authentication, network restrictions, and security controls.
- Avoid entering secrets, API keys, passwords, or other sensitive information into prompts.

## Limitations

- The assistant's answers depend on the selected model and may contain incorrect or insecure code.
- The current implementation uses a fixed local Ollama endpoint.
- The application does not currently include code execution, file uploads, IDE integration, authentication, persistent chat storage, or conversation export.
- Conversation history is passed during the active Gradio chat session; no database is configured.
- The application currently handles Ollama connection errors, but other API or streaming errors may still need additional handling.

## Future Improvements

- Add syntax-highlighted code blocks and one-click code copying.
- Support multiple Ollama models with automatic model discovery.
- Add chat export and persistent conversation history.
- Add file upload for code review and explanation.
- Add configurable Ollama host and connection timeout.
- Improve error handling for malformed streaming responses and missing models.
- Add unit tests and application logging.
- Add optional authentication before enabling access beyond localhost.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push the branch: `git push origin feature/your-feature`.
5. Open a Pull Request.

## Author

**Tauhidul Islam Topu**

- GitHub: [@Tauhid-Topu-007](https://github.com/Tauhid-Topu-007)

## Acknowledgements

- [Ollama](https://ollama.com/) for local model serving.
- [Meta AI](https://ai.meta.com/) for Code Llama.
- [Gradio](https://www.gradio.app/) for the interactive chat interface.

## License

No license file is currently included in this repository. Unless a license is added, the repository's source code is not explicitly granted an open-source license. The Code Llama model and its usage are subject to the applicable model license and acceptable-use terms. See the [Code Llama resources](https://github.com/meta-llama/codellama) for details.
