from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_ollama.llms import OllamaLLM

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 0.7

@app.get("/")
def health():
    return {"ok": True}


@app.post("/llm")
async def generate_response(request: PromptRequest):
    llm = OllamaLLM(
        model="mistral:7b",
        temperature=request.temperature,
        base_url="http://localhost:11434"
    )

    response = llm.invoke(request.prompt)
    return {"response": response}
