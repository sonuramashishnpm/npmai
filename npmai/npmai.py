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
        payload = {
            "prompt": prompt,
            "model": self.model,
            "temperature": self.temperature,
            "validated_schema":self.validated_schema,
        }
        response = requests.post(self.api, json=payload)
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
    def __init__(self, files,query=None,DB_PATH=None,temperature=None,model=None):
        self.files=files
        self.query=query
        self.db_path=DB_PATH
        self.temperature=temperature
        self.model=model
    def send(self):
        files=self.files
        DB_PATH=self.db_path
        query=self.query
        model=self.model
        temperature=self.temperature
        data={
            "query":query,
            "DB_PATH":DB_PATH,
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


