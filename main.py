from pydantic import BaseModel, create_model, ValidationError
import httpx, json
from typing import Annotated, Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
import fitz
import pytesseract
import numpy as np
from pdf2image import convert_from_bytes

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.3
    validated_schema: Optional[Dict[str, Any]] = None

Model_in_Use=[]

Model_links = {
    "llama3.2": "https://sonuramashish22028704-npmai.hf.space/llm",
    "codellama:7b-instruct":"https://sonuramashish22028704-npmai.hf.space/llm",
    "gemma2:9b":"https://sonuramashish22028704-npmai.hf.space/llm",
    "mistral:7b":"https://sonuramashish22028704-npmai.hf.space/llm",
    "qwen2.5-coder:7b":"https://sonuramashish22028704-npmai.hf.space/llm",
    "phi3:medium":"https://sonuramashish22028704-npmai.hf.space/llm",
    "falcon:7b-instruct":"https://sonuramashish22028704-npmai.hf.space/llm",
    "maxkb/baichuan2:13b-chat":"https://sonuramashish22028704-npmai.hf.space/llm",
    "internlm2:7b":"https://sonuramashish22028704-npmai.hf.space/llm",
    "vicuna:7b":"https://sonuramashish22028704-npmai.hf.space/llm",
}

timeout = httpx.Timeout(
    connect=10.0,  # connection ka max time
    read=120.0,    # response read karne ka max time
    write=10.0,    # request bhejne ka max time
    pool=60.0      # connection pool wait
)

@app.post("/llm")
async def handler(data: LLMRequest):
    if len(data.prompt) >= 50000:
        raise HTTPException(400, "Prompt too long")

    if data.model not in Model_links:
        raise HTTPException(400, "Model not supported")

    if data.model not in Model_in_Use:
        Model_in_Use.append(data.model)
        payload = { "prompt": data.prompt, "temperature": data.temperature, }
        url = Model_links[data.model]

        try:
          async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
        except Exception as e:
          return e
        finally:
          if data.model in Model_in_Use:
            Model_in_Use.remove(data.model)
        try:
          raw_output = response.json()["response"]
        except:
          raw_output = response.text

        if not data.validated_schema:
          return {"response":raw_output}

        try:
          DynamicSchema = create_model("DynamicSchema", **data.validated_schema)
          parsed = json.loads(raw_output)
          validated = DynamicSchema(**parsed)
          return validated.dict()
        except (json.JSONDecodeError, ValidationError) as e:
          raise HTTPException(500, f"LLM output invalid: {raw_output}") # No schema, return raw

        return {"response": raw_output}
    else:
        payload = { "prompt": data.prompt, "temperature": data.temperature, }
        for model in Model_links:
            if model not in Model_in_Use:
                Model_in_Use.append(model)
                url=Model_links[model]
                try:
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.post(url, json=payload)
                except:
                    return "Sorry some problem in server222."
                finally:
                    if model in Model_in_Use:
                        Model_in_Use.remove(model)
                try:
                    raw_output = response.json()["response"]
                except:
                    raw_output = response.text
                
                if not data.validated_schema:
                    return {"response":raw_output}
                
                try:
                    DynamicSchema = create_model("DynamicSchema", **data.validated_schema)
                    parsed = json.loads(raw_output)
                    validated = DynamicSchema(**parsed)
                    return validated.dict()
                except (json.JSONDecodeError, ValidationError) as e:
                    raise HTTPException(500, f"LLM output invalid: {raw_output}") # No schema, return raw
                
                return {"response": raw_output}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    path = await file.read()
    doc = fitz.open(stream=path,filetype="pdf")
    text = []
    for p in doc:
        t = p.get_text().strip()
        if t:
            text.append(t)
    if text:
        return "\n".join(text)
    images = convert_from_bytes(path)
    return "\n".join(pytesseract.image_to_string(img) for img in images)
    
