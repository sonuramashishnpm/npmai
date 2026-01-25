# 🚀 npmai 
**By Sonu Kumar Ramashish**

[![PyPI version](https://img.shields.io)](https://pypi.org/project/npmai/0.1.2)
[![License: MIT](https://img.shields.io)](https://opensource.org)

`npmai` is a lightweight Python package designed to bridge the gap between users and open-source LLMs. Connect with **Ollama** and 10+ other powerful models instantly—**no installation, no login, and no API keys required.**

---

## ✨ Features

- 🔗 **Zero Setup:** No local Ollama installation or complex API signups needed.
- 🤖 **Multi-Model Support:** Execute prompts across 10+ open-source models simultaneously.
- 🧠 **Built-in Memory:** (New in v0.1.2) Native memory support—no need for external Agentic frameworks.
- ⚡ **Framework Ready:** Fully compatible with **LangChain**, **CrewAI**, and other orchestration tools.
- 🛠️ **Universal API:** Access via Python, JavaScript, C++, Java, or C.

---

## 🖥️ Supported Models

| Model Name | Description |
| :--- | :--- |
| `llama3.2` | Meta's latest powerful small model |
| `gemma-2-instruct-9b` | Google's high-performance open model |
| `qwen-2.5-coder-7b` | Alibaba's elite coding assistant |
| `mistral-7b-instruct` | Versatile and efficient instructor model |
| `phi-3-medium` | Microsoft's highly capable reasoning model |
| *And many more...* | Falcon, Baichuan-2, InternLM, Vicuna |

---

## ⚙️ Installation

Install via pip in seconds:

```bash
pip install npmai
Use code with caution.

Tip for Python 3.13+: Use py -3.13 -m pip install npmai
💡 Quick Start (Python)
python
from npmai import Ollama

# Initialize the LLM
llm = Ollama()      

# Simple invocation
response = llm.invoke("What is the future of AI?", model="llama3.2")
print(response) 

🌐 API Usage (Other Languages)
If you aren't using Python, hit our global endpoint:
POST https://npmai-api.onrender.com
🟡 JavaScript
javascript
const response = await fetch("https://npmai-api.onrender.com", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "Hello! Who are you?",
    model: "llama3.2",
    temperature: 0.4
  })
});
const data = await response.json();
console.log(data.response);

🔵 C++
cpp
nlohmann::json payload = {
    {"prompt", "Explain quantum physics."},
    {"model", "llama3.2"},
    {"temperature", 0.4}
};
auto res = cli.Post("/llm", payload.dump(), "application/json");

🆕 Latest Update: Version 0.1.3
We have introduced Native Memory! You no longer need to manually manage chat history or rely on complex Agentic frameworks. npmai now handles context persistence internally, allowing for seamless continuous conversations.
⚠️ Important Notes
Experimental Use: This project is designed for educational purposes, small-scale experimentation, and demo projects.
Scale Responsibly: For high-volume production traffic, please support the original AI researchers and infrastructure providers.
🔗 Resources
Documentation: npmai.netlify.app
API Endpoint: npmai-api.onrender.com
Developed with ❤️ to make AI accessible to everyone.
Developer and Maintainer:- Sonu Kumar

