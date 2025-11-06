import importlib.util
import os

pyc_path = os.path.join(os.path.dirname(__file__), "__pycache__", "main.cpython-311.pyc")
spec = importlib.util.spec_from_file_location("main", pyc_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

from main import GeminiAIMode, Gemini, ChatGPT, Grok, Perplexity
__all__ = ["GeminiAIMode", "Gemini", "ChatGPT", "Grok", "Perplexity"]
