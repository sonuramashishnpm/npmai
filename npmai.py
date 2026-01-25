from langchain_core.language_models.llms import LLM
from typing import Optional, List, Union, Iterator, Dict, Any
import requests
import json

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
    def __init__(self, user_id):
        self.filename = f"memory_{user_id}.json"

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

# Call Code
if __name__ == "__main__":
    llm=Ollama(
        model="llama3.2",
        temperature=0.8,
        )
    prompts=input("Enter Your Query:")
    response=llm.invoke(prompts)
    print(response)
