from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_ollama.llms import OllamaLLM
from tavily import TavilyClient
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 0.7

@app.get("/")
def health():
    return {"ok": True}

def search_tool(query:str):
    api_key= os.environ.get("TAVILY_API_KEY")
    client = TavilyClient(api_key)
    response = client.search(
        query=query,
        include_answer="advanced",
        search_depth="advanced"
    )
    return response
    
@app.post("/llm")
async def generate_response(request: PromptRequest):
    llm = OllamaLLM(
        model="internlm2:7b",
        temperature=request.temperature,
        base_url="http://localhost:11434"
    )

    system_prompt = """
    Hey you are a very good assistant that answer users query and tasks.
    """

    tool_prompt = """
    You have a Tool also that you can use but only use when you need do not use for every query.
    If you want to search about query when you are sure that you do not know about the query or the data you have is outdated then call this tool:-
    Tool Name:- Search_tool
    Description:- It Searches on internet and return latest information and those information that a LLM do not know.
    How to use:- If LLM wants to search then it should only return "Search (query)" here you need to write Search in same way in the query word you are seeing in bracket
    you do not have to use bracked just write what you want to search.
    Example:- Like a LLM wants to use tool it will return this:- Search Who is the Prime Minister of India in 2026
    Note:- what if you are not calling any tool so do not use Search Keyword in starting of response of User Query.
    """
    response = llm.invoke(f'{system_prompt},{tool_prompt},Now this is User Query:-{request.prompt}')
    print("RESPONSE")
    print(response)
    if "Search " in response:
        new_query = response.removeprefix("Search ")
        print("NEW_QUERY")
        print(new_query)
        search_response = search_tool(query=new_query)
        print("SEARCH_RESPONSE")
        print(search_response)
        new_response = llm.invoke(f"Extra_information:- {search_response} User-Query:- {request.prompt}")
        return {"response": new_response}
    else:
        return {"response": response}

@app.post("/baichuan")
async def generate_response(request: PromptRequest):
    llm = OllamaLLM(
        model="maxkb/baichuan2:13b-chat",
        temperature=request.temperature,
        base_url="http://localhost:11434"
    )

    system_prompt = """
    Hey you are a very good assistant that answer users query and tasks.
    """

    tool_prompt = """
    You have a Tool also that you can use but only use when you need do not use for every query.
    If you want to search about query when you are sure that you do not know about the query or the data you have is outdated then call this tool:-
    Tool Name:- Search_tool
    Description:- It Searches on internet and return latest information and those information that a LLM do not know.
    How to use:- If LLM wants to search then it should only return "Search (query)" here you need to write Search in same way in the query word you are seeing in bracket
    you do not have to use bracked just write what you want to search.
    Example:- Like a LLM wants to use tool it will return this:- Search Who is the Prime Minister of India in 2026
    Note:- what if you are not calling any tool so do not use Search Keyword in starting of response of User Query.
    """
    response = llm.invoke(f'{system_prompt},{tool_prompt},Now this is User Query:-{request.prompt}')
    print("RESPONSE")
    print(response)
    if "Search " in response:
        new_query = response.removeprefix("Search ")
        print("NEW_QUERY")
        print(new_query)
        search_response = search_tool(query=new_query)
        print("SEARCH_RESPONSE")
        print(search_response)
        new_response = llm.invoke(f"Extra_information:- {search_response} User-Query:- {request.prompt}")
        return {"response": new_response}
    else:
        return {"response": response}
