# 🚀 npmai 
**By Sonu Kumar (Viral Boy)**

[![PyPI version](https://img.shields.io)](https://pypi.org/project/npmai/0.1.6)
[![License: MIT](https://img.shields.io)](https://opensource.org)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sonuramashishnpm/npmai)

`npmai` is a lightweight Python package designed to bridge the gap between users and open-source LLMs. Connect with **Ollama** and 10+ other powerful models instantly—**no installation, no login, and no API keys required, and help in development of RAG Agents without installing anything locally or on cloud and it is free without sigin or signup or any type of limit.**

---

## ✨ Features

- 🔗 **Zero Setup:** No local Ollama installation or complex API signups needed.
- 🤖 **Multi-Model Support:** Execute prompts across 10+ open-source models simultaneously.
- 🧠 **Built-in Memory:** (New in v0.1.3) Native memory support—no need for external Agentic frameworks.
- 🕵️‍♂️🔍📑 **RAG Frame-Work:** **no need to install Whisper or any model locally,no need to write code for the pdf,image,video,yt-video to text  just use npmai**
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

## Workflow:-

**npmai**
<img src="https://i.ibb.co/NgChKgHP/npmai.png" alt="Example Screenshot" width="700" style="display: block; margin: 0 auto; margin-left:20px">

**Rag**
<img src="https://i.ibb.co/qYJd6Nhw/NPMAI-Rag-API-Pipeline.png" alt="Example Screenshot" width="700" style="display: block; margin: 0 auto; margin-left:20px">


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
```
🆕 Latest Update: Version 0.1.6
In this update we added the try and except for api hitting and added huggingface api endpoints as fallback.
version 0.1.5 --->> Just fixed some bugs and added link as a parameter in Rag class
version 0.1.4 --->> Now you do not need to write code for RAG tools like pdf,image,video,audio,yt-video to text and no need to load whisper and other requirements locally no local process everything on cloud in free without any signup or singin or key hurdles.
⚠️ Important Notes
Please star our project on Github please.
🔗 Resources
Documentation: npmai.netlify.com
API Endpoint: npmai-api.onrender.com/llm
Developed with ❤️ to make AI accessible to everyone.
Developer and Maintainer:- Sonu Kumar

