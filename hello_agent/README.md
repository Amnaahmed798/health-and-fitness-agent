# 🤖 Async Hello Agent (with Gemini API)

## 📖 Overview

**Async Hello Agent** is an asynchronous AI assistant powered by the **Google Gemini API**, interfaced through an OpenAI-compatible client. This project demonstrates how to integrate Gemini with Python using the `agents` framework, and how to run a simple prompt query in an async environment.

The agent is set up to respond to a sample question:
> "Tell me about recursion in programming."

When run, it uses the Gemini model to generate an answer and prints it to the console.

---

## 📦 Features

- Asynchronous execution with `asyncio`
- Gemini API integration via OpenAI-compatible client
- Environment variables for secure API key handling
- Customizable agent instructions and prompts

---

## 🚀 How to Run

### 1. 📁 Setup Your Environment

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```
Replace `your_gemini_api_key_here` with your actual Gemini API key.

### 2. 📦 Install Dependencies

Make sure you have the required libraries installed. If not, install them using:

```bash
pip install python-dotenv asyncio
```
Also ensure that the `agents` package and any required dependencies (like `openai`, `httpx`, etc.) are installed.

### 3. ▶️ Run the Agent

Use `uvicorn` if you're running a web app, but this project is a pure script. Run it using:

```bash
python main.py
```
You'll see the output in the terminal, for example:

```vbnet
Function calls itself,
Looping in smaller pieces,
Endless by design.
```

## 🧠 How It Works

1. Loads the Gemini API key from the `.env` file.
2. Creates an `AsyncOpenAI` client using Gemini's OpenAI-compatible endpoint.
3. Wraps the Gemini model in an `OpenAIChatCompletionsModel`.
4. Defines a simple agent using the `agents` framework with custom instructions.
5. Sends a prompt asynchronously and prints the final response.

## 📚 Reference

- [Gemini API Docs](https://ai.google.dev/gemini-api/docs/openai)
- Agents Framework (if using a custom or open-source package)

## 🛠 Customization Ideas

- Modify the prompt and instructions.
- Extend the script into a web API using FastAPI + uvicorn.
- Add logging and error handling.
- Turn into a chatbot or command-line assistant.

## 🔒 Notes

- Keep your `.env` file safe and do not commit it to version control.
- Ensure your API key has the necessary permissions for the Gemini API.