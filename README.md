# 🚀 npmai 
**By Sonu Kumar (Viral Boy)**

<a href="https://pypi.org/project/npmai"><img src="https://img.shields.io/pypi/v/npmai?logo=pypi&style=for-the-badge" /></a>
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sonuramashishnpm/npmai)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/npmai?period=total&units=INTERNATIONAL_SYSTEM&left_color=ORANGE&right_color=BRIGHTGREEN&left_text=downloads)](https://pepy.tech/projects/npmai)

`npmai` is a lightweight Python package designed to bridge the gap between users and open-source LLMs. 

Connect with **Ollama** and 10+ other powerful models instantly—**no installation, no login, and no API keys required, and help in development of RAG Agents without installing anything locally or on cloud and it is free without sigin or signup or any type of limit.**

---

## ✨ Features

- 🔗 **Zero Setup:** No local Ollama installation or complex API signups needed.
- 🤖 **Multi-Model Support:** Execute prompts across 10+ open-source models simultaneously.
- 🧠 **Built-in Memory:** (New in v0.1.3) Native memory support—no need for external Agentic frameworks.
- 🕵️‍♂️🔍📑 **RAG Frame-Work:** **no need to install Whisper or any model locally,no need to write code for the pdf,image,video,yt-video to text  just use npmai**
- 🔍📑 **Vectorised Database** **Now you can store your any all type of files in vectorised form through npmai for free of cost unlimited time**
- ⚡ **Framework Ready:** Fully compatible with **LangChain**, **CrewAI**, and other orchestration tools.
- 🛠️ **Universal API:** Access via Python, JavaScript, C++, Java, or C.
- 🔍 Tavily Integrated and also integrating MCP Servers and advance tools to make LLM more powerfull

---

## 🖥️ Supported Models

| Model Name | Description |
| :--- | :--- |
| `llama3.2` | Meta's latest powerful small model |
| `gemma-2-instruct-9b` | Google's high-performance open model |
| `qwen-2.5-coder-7b` | Alibaba's elite coding assistant |
| `mistral-7b-instruct` | Versatile and efficient instructor model |
| `phi-3-medium` | Microsoft's highly capable reasoning model |
| `Falcon` | From UAE ,TII |
| `Baichuan-2` | Baichuan from China |
| `InternLM` | From Sanghai AI Laboratory |
| `Vicuna` | From LMSYS Org |
| `gemma3:12b` | A latest AI Model by Google which has knowledge cutoff of 2026 also ***Latest AI Model in NPMAI ECOSYSTEM**|

---

## Workflow:-

### npmai
<img src="https://i.ibb.co/NgChKgHP/npmai.png" alt="Example Screenshot" width="700" style="display: block; margin: 0 auto; margin-left:20px">

### Rag
<img src="https://i.ibb.co/W43CqndR/NPMAI-RAG-API-Pipleline.png" alt="Example Screenshot" width="1100" style="display: block; margin: 0 auto; margin-left:20px">


## npmai Ecosystem:-

Here <a href="https://npmai.netlify.com"><img src="https://img.shields.io/badge/npmai-blue" /></a> is the main core component of **NPMAI ECOSYSTEM** in Ecosystem following products are:-

**1.NPM-Rag-A.I**:-NPM Rag A.I is a beautiful, easy-to-use web application that lets you instantly create and talk to your own private or public knowledge bases using RAG (Retrieval-Augmented Generation).

Visit:- <a href="https://npmragai.onrender.com"><img src="https://img.shields.io/badge/NPM%20Rag%20AI-blue" /></a> 

**2.NPM-Journalist**:-You can raise voice to Government without getting traced,safe & secure journalism.

Visit:- <a href="https://npmjournalist.onrender.com"><img src="https://img.shields.io/badge/NPM%20Journalist-blue" /></a> 

**3.NPM-AutoCode-A.I**:- Full Autonomous agent where A.I will write code to auotmate PC and execute debug and before execution of any code there will be a safety check,full secure.

Visit:- <a href="https://npmcodeai.netlify.com"><img src="https://img.shields.io/badge/NPM%20AutoCode%20AI-blue" /></a> 

**4.NPM-Youtube-Automation**:-Just give us Video and Thumbnail and go to sleep your video will automatically uploaded to Youtube with full meta-data including captions.(Future update:- Your video or any post will be uploaded to all social media platforms from Facebook to X to insta to all).

Visit:- <a href="https://npmyt.onrender.com"><img src="https://img.shields.io/badge/NPM%20Youtube%20Automation-blue" /></a> 

**5.NPM-Debater-A.I**:-You can enjoy debate of 4 AI models just enter topic and enjoy infinite debate arena.

Visit:- <a href="https://npmdebateai.onrender.com"><img src="https://img.shields.io/badge/NPM%20Debater%20AI-blue" /></a> 

**6.NPM-Legal-A.I**:-Legal Chatbot with specific models,processings for free supports all documents of users (Currently it only support Indian Laws).

Visit:- <a href="https://npmlegalai.onrender.com"><img src="https://img.shields.io/badge/NPM%20Legal%20AI-blue" /></a> 

**7.NPM-Business-Analysis-A.I**:-Business Analysis AI where you will explain your business and it will guide you in making plans (Future Updates:- ***NPM-Youtube-Automation*** and ***npmai-RAG*** will be integrated.)

Visit:- <a href="https://npmbusinessai.netlify.app/"><img src="https://img.shields.io/badge/NPM%20Business%20Analysis%20AI-blue" /></a> 

**8.NPM-Data-A.I**:-It will analyse your Bank Account transaction history and it will give advice related to your financial future and conditions.

Visit:- <a href="https://npmdata.streamlit.app"><img src="https://img.shields.io/badge/NPM%20Data%20AI-blue" /></a> 

***Note:- All projects are free and deployed and production ready.***

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
🆕 Latest Update: Version 0.1.8

In this update :-
1. Integrated Supabase for long term storage of vecorised Documents, this integration is done in Huggingface Server where npmai send request for Rag processes.
2. Added a method in Rag class of npmai sdk named "vector_db_use".
3. Updated parameters of Rag class to make compatible with supabase integration on Huggingface Server.
4. Updated Docstrings for Rag class.

version 0.1.7 --->> Updated parameters of Rag class for sending multiple files of all type at once and also added a clear_memory method in Memory class to remove memory files and added docstrings description in every class Ollama,Memory,Rag.

version 0.1.6 --->> Added try and except for api hitting and added huggingface api endpoints as fallback.

version 0.1.5 --->> Just fixed some bugs and added link as a parameter in Rag class.

version 0.1.4 --->> Now you do not need to write code for RAG tools like pdf,image,video,audio,yt-video to text and no need to load whisper and other requirements locally 
no local process everything on cloud in free without any signup or singin or key hurdles.

## Important Update in NPMAI RAG:-

# 🚀 NPMAI Update: Advanced RAG & Refine Architecture

We have officially upgraded the **NPMAI Ecosystem** to a more intelligent, cost-efficient, and "Product-Ready" pipeline. These updates move beyond basic RAG into **High-Performance Agentic Retrieval**.

---

### 🔍 1. Dynamic K-Context Retrieval (70% Coverage)

**The Problem:** 
Standard RAG systems use a fixed `k` value (e.g., `k=4`). This is inefficient—it provides too little context for large documents (missing facts) and too much "noise" for tiny documents (wasting tokens).

**The Solution:** 
I have engineered a **Proportional Scaling Logic** that calculates the optimal number of chunks to retrieve based on the actual density of your vectorized database.

*   **Logic:** `dynamic_k = max(1, int(total_chunks * 0.70))`
*   **How it works:**
    *   **Short Documents:** If your database has only 2 chunks, the system retrieves only those 2.
    *   **Large PDFs:** If your PDF generates 100 chunks, the system automatically scales up to retrieve **70 relevant chunks** ($k=70$).
*   **The Impact:** This ensures the AI always sees a **statistically significant slice** of the knowledge base, adapting perfectly to any document size.

---

### 🔄 2. Sliding Window Batch-Refinement (3-Chunk Window)

**The Problem:** 
Traditional "Refine" strategies process one chunk at a time. This is incredibly slow because it makes $N$ separate API calls. For a 30-chunk document, the user waits too long.

**The Solution:** 
I have implemented a **Sliding Window Batch-Refine** system that processes chunks in groups of 3 instead of 1.

*   **Logic:** `for i in range(0, total_chunks, 3):`
*   **How it works:**
    *   Instead of making a single LLM call for every 1,000 characters, the system sends a **batch of 3 related chunks** (3,000 characters) in one go.
    *   It uses the previous answer as a "Running Memory" to merge new information from the current 3-chunk batch.
*   **The Impact:** 
    *   **3x Faster Execution:** We have reduced total API latency by **66%**.
    *   **Improved Coherence:** The AI sees a broader context ($3,000$ chars vs $1,000$ chars), allowing it to spot connections between facts that are split across neighboring chunks.

---

### ☁️ 3. Infrastructure: Persistent Supabase Integration (v0.1.8)

We have successfully integrated **Supabase Object Storage** to move from temporary memory to **Persistent Knowledge Bases**.

*   **Vector Persistence:** All `.faiss` and `.pkl` index files are now automatically uploaded to a secure Supabase bucket.
*   **Multi-Platform Access:** This allows **NPM-Rag-AI**, **NPM-AutoCode-AI**, and the **npmai SDK** to share and load the same vectorized data from anywhere in the world.

---
**Summary:** 
These architectural changes make **NPMAI** one of the most efficient open-source RAG frameworks available for developers who need **Speed + Accuracy** without the high cost of standard 1-by-1 refinement.

⚠️ Important Notes:-

Please star our project on Github please.

🔗 Resources

Documentation: npmai.netlify.com

API Endpoint: npmai-api.onrender.com/llm

Developed with ❤️ to make AI accessible to everyone.

Developer and Maintainer:- Sonu Kumar
