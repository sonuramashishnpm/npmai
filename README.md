npmai

npmai (by Sonu Kumar Ramashish) is a lightweight Python package that seamlessly connects LangChain with real-time web-based LLMs like Gemini, ChatGPT, Grok, Mistral and Perplexity and a IMage Generation model via Selenium automation.

🚀 Features

Execute prompts on multiple LLMs simultaneously: Gemini, ChatGPT, Grok, Perplexity, Mistral, Image.

Fully LangChain-compatible interface.

Simple and intuitive invoke() API for instant responses.

Browser automation with headless Chrome via Selenium.

Supports continuous conversation mode for long-running interactions with ChatGPT or Gemini.

Encourages responsible usage—please respect AI companies like OpenAI, Google, X AI, Perplexity, Mistral and support them if used at scale.

⚙️ Installation pip install npmai

pip install npmai

💡 How to Use

Import the models you need—either one, two, or all:

To use:
1.ChatGPT:
from npmai import ChatGPT
llm=ChatGPT()
print(llm.invoke("Hello GPT how are you"))

2.Gemini:
from npmai import Gemini
llm=Gemini()
print(llm.invoke("Hello Gemini what's today news"))

3.Grok:
from npmai import Grok
llm=Grok()
print(llm.invoke("Hello Grok what is calculus and who was euclid"))

4.Perplexity:
from npmai import Perplexity
llm=Perplexity()
print(llm.invoke("Hello perplexity what do you think about recent news about USA Donald Trump"))

5.Mistral:
from npmai import Mistral
llm=Mistral()
print(llm.invoke("Hello mist write a pythond code using turtle that animate a tree"))

6.GeminiAIMode:
from npmai import GeminiAIMode
llm=GeminiAIMode()
print(llm.invoke("Hello can you who developer npmai library"))

7.Image:
from npmai import Image
llm=Image()
print(llm.invoke("Hey generate a image in that a dog is standing on moon"))


#Latest Update : version 0.0.7 Here you will get Mistral also.

⚠️ Important Notes

Designed for educational and small-scale experimentation.

If using at a larger scale, consider supporting the original AI platforms—they invest heavily in research and infrastructure.

Continuous mode allows extended conversations, but use responsibly to avoid overloading web-based LLM services.

✅ npmai makes it effortless to connect web-based AI models with Python, bringing automation, experimentation, and LangChain integration together in a single, easy-to-use package.
