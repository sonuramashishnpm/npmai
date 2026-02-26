from langchain_core.language_models.llms import LLM
from typing import Optional, List, Union, Iterator, Dict, Any
import requests
import json
import os

PromptType = Union[str, List[str], dict]

class Ollama(LLM):
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

class Rag:
    def __init__(self, files,query=None,DB_PATH=None,link=None,temperature=None,model=None):
        self.files=files
        self.query=query
        self.db_path=DB_PATH
        self.link=link
        self.temperature=temperature
        self.model=model
    def send(self):
        files=self.files
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
        HF_API="https://sonuramashish22028704-npmeduai.hf.space/ingestion"
        with open(files,"rb") as f:
            file={"file":f}
            res=requests.post(HF_API,data=data,files=file,timeout=600)
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
