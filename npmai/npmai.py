from langchain_core.language_models.llms import LLM
from typing import Optional, List, Union, Iterator, Dict, Any
import requests
import json
import os

PromptType = Union[str, List[str], dict]

class Ollama(LLM):
    """
    A resilient LLM wrapper for NPMAI providing access to 10+ Open Source models.
    
    This class features a dual-gateway architecture:
    1. Primary API: Attempts to process requests via https://npmai-api.onrender.com.
    2. Failover System: If the primary gateway is down, it silently switches to 
       dedicated Hugging Face endpoints based on the selected model.
    
    Key Capabilities:
    - High Availability: Automatic retry logic ensures minimal downtime.
    - Model Variety: Supports Llama 3.2, Qwen 2.5, Vicuna, Gemma 2, InternLM2, Mistral, and more.
    - Structured Output: Accepts a 'validated_schema' to enforce specific JSON formats.
    - Versatile Input: The 'invoke' method handles strings, lists, or dictionary prompts.
    """
    model: str = "llama3.2"
    temperature: float = 0.3
    validated_schema: Optional[Dict[str,Any]]=None
    api: str = "https://npmai-api.onrender.com/llm"
    
    @property
    def _llm_type(self) -> str:
        return "npmai"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        Model_links = {
            "llama3.2": "https://sonuramashish22028704-npmai.hf.space/llm",
            "qwen2.5-coder:7b":"https://sonuramashish22028704-npmai.hf.space/qwen",
            "vicuna:7b":"https://sonuramashish22028704-vicuna7b.hf.space/llm",
            "gemma2:9b":"https://sonuramashish22028704-vicuna7b.hf.space/gemma",
            "internlm2:7b":"https://sonuramashish22028704-internlm27b.hf.space/llm",
            "maxkb/baichuan2:13b-chat":"https://sonuramashish22028704-internlm27b.hf.space/baichuan",
            "falcon:7b-instruct":"https://sonuramashish22028704-falcon7binstruct.hf.space/llm",
            "codellama:7b-instruct":"https://sonuramashish22028704-falcon7binstruct.hf.space/codellama",
            "mistral:7b":"https://sonuramashish22028704-mistral7b.hf.space/llm",
            "phi3:medium":"https://sonuramashish22028704-phi3medium.hf.space/llm",
        }
        
        payload = {
            "prompt": prompt,
            "model": self.model,
            "temperature": self.temperature,
            "validated_schema":self.validated_schema,
        }

        fallback_payload ={
            "prompt":prompt,
            "temperature":self.temperature,
        }
        try:
            response = requests.post(self.api, json=payload)
            response.raise_for_status()
        except:
            api = Model_links[self.model]
            response = requests.post(api, json=fallback_payload)
            response.raise_for_status()
            
        data=response.json()
        if "response" in data:
            return data["response"]
        return json.dumps(data)
        


    def invoke(self, prompt: PromptType):
        if isinstance(prompt, list):
            prompt = "\n".join(map(str, prompt))
        elif isinstance(prompt, dict):
            prompt = json.dumps(prompt)

        return self._call(prompt)
        
class Memory:
    """
    A lightweight persistent memory system for AI Agents to maintain conversation context.

    This class enables agents to remember past interactions by storing them in a local 
    JSON-based file system. It is designed to be easily integrated into any workflow 
    where long-term or session-based memory is required.

    Key Features:
    - Custom Persistence: Creates a unique .json file based on the provided user_custom_file name.
    - Context Management: save_context() appends new Human-AI interactions to the history.
    - History Retrieval: load_memory_variables() parses the stored data into a formatted 
      string for easy injection into LLM prompts.
    - Fault Tolerance: Safely handles empty files and skips corrupted JSON lines during loading.
    - Clear Memory easily.
    """
    def __init__(self, user_custom_file):
        self.filename = f"memory_{user_custom_file}.json"

    def save_context(self, user_input, ai_output):
        with open(self.filename, "a") as data:
            json.dump({"Human": user_input, "AI": ai_output}, data)
            data.write("\n")

    def load_memory_variables(self):
        string_history = ""
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, "r") as data:
                for line in data:
                    try:
                        ldata = json.loads(line)
                        string_history += f"Human: {ldata['Human']}\nAI: {ldata['AI']}\n"
                    except json.JSONDecodeError:
                        continue
        return string_history

    def clear_memory(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            return "Sorry either your memory file had been deleted or not created"

class Rag:
    """
    An all-in-one Retrieval-Augmented Generation (RAG) and File-to-Text conversion engine.

    This class serves two primary purposes:
    1. Unified File Conversion: Converts PDFs, images, local videos, and YouTube videos into text.
    2. Automated RAG Pipeline: When a query and DB_PATH are provided, it automatically handles 
       text extraction, vector database ingestion, and LLM reasoning without requiring 
       manual LLM integration.
    3.Every thing is on cloud without any local installation or load in FREE OF COST UNLIMITED.

    Key Logic:
    - Smart Defaults: If DB_PATH and query are provided, the system defaults to 'llama3.2' 
      and a temperature of 0.5 unless otherwise specified.
    - Context-Aware Mode: If DB_PATH and query are omitted, the class functions as a pure 
      extraction tool, returning only the text content of the files.
    - Multi-Source Support: Accepts local file paths and external links (e.g., YouTube) 
      via a single interface.
    """
    def __init__(self, files,query=None,DB_PATH=None,link=None,temperature=None,model=None):
        self.files=files
        self.files_to_send=[]
        self.query=query
        self.db_path=DB_PATH
        self.link=link
        self.temperature=temperature
        self.model=model
    def send(self):
        files=self.files
        files_to_send=self.files_to_send
        DB_PATH=self.db_path
        link=self.link
        query=self.query
        model=self.model
        temperature=self.temperature
        data={
            "query":query,
            "DB_PATH":DB_PATH,
            "link":link,
            "temperature":temperature,
            "model":model
        }
        for path in files:
          files_to_send.append(('file', open(path, 'rb')))
          
        HF_API="https://sonuramashish22028704-npmeduai.hf.space/ingestion"
        
        res=requests.post(HF_API,data=data,files=files_to_send,timeout=600)
        response=str(res)
        try:
          return {"response":res.json().get("response")}
        except:
          return res
        

# Call Code
if __name__ == "__main__":
    llm=Ollama(
        model="llama3.2",
        temperature=0.4,
        )
    prompts=input("Enter Your Query:")
    response=llm.invoke(prompts)

    print(response)
