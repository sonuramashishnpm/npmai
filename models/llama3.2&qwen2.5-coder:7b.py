from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_ollama.llms import OllamaLLM

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 0.5

@app.get("/")
def health():
    return {"ok": True}


@app.post("/llm")
async def generate_response(request: PromptRequest):
    llm = OllamaLLM(
        model="llama3.2",
        temperature=request.temperature,
        base_url="http://localhost:11434"
    )

    response = llm.invoke(request.prompt)
    return {"response": response}


@app.post("/qwen")
async def qwen_generate_response(request:PromptRequest):
    llm = OllamaLLM(
        model="qwen2.5-coder:7b",
        temperature=request.temperature,
        base_url="http://localhost:11434"
    )

    response= llm.invoke(request.prompt)
    return {"response":response}

