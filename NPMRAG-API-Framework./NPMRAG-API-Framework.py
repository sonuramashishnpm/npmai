from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama.llms import OllamaLLM
from fastapi import FastAPI, UploadFile, File, Form 
from fastapi.responses import JSONResponse
from moviepy.editor import VideoFileClip
from pdf2image import convert_from_path
from pydantic import BaseModel
from fastapi import FastAPI
from npmai import Ollama
from PIL import Image
import numpy as np
import pytesseract
import threading
import whisper
#import yt_dlp
import fitz
import time
import cv2
import os

app=FastAPI()

os.environ["CUDA_VISIBLE_DEVICES"] = ""


_whisper_model = None
_whisper_lock = threading.Lock()

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        with _whisper_lock:
            if _whisper_model is None:
                _whisper_model = whisper.load_model("base")
    return _whisper_model


#FUNCTIONS

def pdf_has_text(path):
    print("has_text")
    doc=fitz.open(path)
    for i in range(len(doc)):
        page=doc[i]
        text=page.get_text().strip()
        if text:
            print("texttrue")
            return True
    return False

@app.post("/pdfetext")
def extractable_text(path,DB_PATH=None,query=None, temperature=None, model=None):
    print("Extracting")
    doc=fitz.open(path)
    full=[]
    for page in doc:
        full.append(page.get_text())
    text="\n".join(full)
    if query is not None and DB_PATH is not None:
        print("query")
        return retrieval(DB_PATH=DB_PATH,query=query,texts=text,temperature=temperature,model=model)
    else:
        print("else")
        return text

def preprocess_for_ocr(path):
    img=cv2.imread(path,cv2.IMREAD_COLOR)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    h,w=gray.shape
    if w < 1000:
        gray=cv2.resize(gray,(int(w*2),int(h*2)),interpolation=cv2.INTER_CUBIC)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

@app.post("/pdfstext")
def pdf_scanned_to_text(pdf_path,dpi=300, tesseract_lang='eng',DB_PATH=None,query=None, temperature=None, model=None):
    print("scanning")
    pages = convert_from_path(pdf_path, dpi=dpi)
    print("pages")
    full = []
    for img in pages:
        print("img")
        full.append(pytesseract.image_to_string(img, lang=tesseract_lang, config='--psm 6'))
    text="\n\n".join(full)
    print(text)
    if query is not None and DB_PATH is not None:
        print("query")
        return retrieval(DB_PATH=DB_PATH,query=query,texts=text,temperature=temperature,model=model)
    else:
        print("elsetext")
        return text

@app.post("/ocr")
def ocr(path,lang="eng",DB_PATH=None,query=None, temperature=None, model=None):
    proc = preprocess_for_ocr(path)
    pil = Image.fromarray(proc)
    full = pytesseract.image_to_string(pil, lang=lang, config='--psm 6')
    if query is not None and DB_PATH is not None:
        return retrieval(DB_PATH=DB_PATH,query=query,texts=full,temperature=temperature,model=model)
    else:
        return full

"""
@app.post("/ytvideo)
def get_transcript(link,output_path,DB_PATH=None,query=None, temperature=None, model=None):
    url = link
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'ignoreerrors': 'only_sample',
        'extractor_args': {'youtube': {'player_client': 'default'}}, 
        'age_limit': 99,
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("\nDownload finished successfully!")
    except Exception as e:
        print(f"\nAn error occurred during download: {e}")
    print("If the error is 'Sign In', you need to provide cookies as mentioned previously.")
    clip=VideoFileClip(output_path)
    audio=clip.audio
    audio.write_audiofile("temp.wav")
    model= get_whisper_model()
    result=model.transcribe("temp.wav")
    text=result["text"]
    if query is not None and DB_PATH is not None:
        return retrieval(DB_PATH=DB_PATH,query=query,texts=text,temperature=temperature,model=model)
    else:
        return text"""

@app.post("/video")
def local_video_processing(video_path,DB_PATH=None,query=None, temperature=None, model=None):
    clip=VideoFileClip(video_path)

    audio=clip.audio
    audio.write_audiofile("temp.wav")

    model= get_whisper_model()
    result=model.transcribe("temp.wav")
    text=result["text"]
    if query is not None and DB_PATH is not None:
        return retrieval(DB_PATH=DB_PATH,query=query,texts=text,temperature=temperature,model=model)
    else:
        return text

@app.post("/text")
def text_processes(path,DB_PATH=None,query=None, temperature=None, model=None):
    with open(path,"r") as f:
        text=f.read()
        if query is not None and DB_PATH is not None:
            return retrieval(DB_PATH=DB_PATH,query=query,texts=text,temperature=temperature,model=model)
        else:
            return text
    

#ROUTING POINT
@app.get("/")
def health():
    return {"ok":True}
    

@app.post("/ingestion")
async def ingest_file(
    query: str = Form(None),
    DB_PATH: str = Form(None),
    file: UploadFile = File(None),
    link: str = Form(None),
    output_path: str = Form(None),
    temperature:float = Form(None),
    model: str = Form(None),
):
    os.makedirs("uploads", exist_ok=True)
    result = None

    # ---------- FILE MODE ----------
    if file:
        contents = await file.read()
        file_path = f"uploads/{file.filename}"
        print("file_path")

        with open(file_path, "wb") as f:
            f.write(contents)

        ext = file.filename.lower().split(".")[-1]

        if ext == "pdf":
            print("pdf")
            if pdf_has_text(file_path):
                result = extractable_text(path=file_path, DB_PATH=DB_PATH, query=query, temperature=temperature, model=model)
                print("yes")
            else:
                result = pdf_scanned_to_text(pdf_path=file_path, DB_PATH=DB_PATH, query=query, temperature=temperature, model=model)
                print('yes2')

        elif ext in ("png", "jpg", "jpeg"):
            result = ocr(path=file_path, DB_PATH=DB_PATH, query=query, temperature=temperature, model=model)

        elif ext == "txt":
            result = text_processes(path=file_path, DB_PATH=DB_PATH, query=query, temperature=temperature, model=model)

        elif ext == "mp4":
            result = local_video_processing(video_path=file_path, DB_PATH=DB_PATH, query=query, temperature=temperature, model=model)
        
        else:
            return JSONResponse({"response": "Unsupported file type"})

    else:
        return JSONResponse({"response": "No input provided"})

    return JSONResponse({"response": result})
        
    """# ---------- LINK MODE ----------
    elif link:
        result = get_transcript(link, DB_PATH, query, output_path)"""


#RETRIEVAL
def retrieval(texts,DB_PATH,query,emb=HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5",model_kwargs={"device":"cpu"},encode_kwargs = {"normalize_embeddings": True},query_instruction="Represent this sentence for searching relevant passages: "), temperature=None, model=None):
  if DB_PATH is not None and query is not None:
      print("1")
      if os.path.exists(DB_PATH):
          vector_db=FAISS.load_local(
              DB_PATH,
              emb,
              allow_dangerous_deserialization=True
          )
          print("2")
          retriever=vector_db.similarity_search(query,k=4)
          return preref(text=retriever,question=query,temperature=temperature,model=model)
      
      else:
          print("3")
          text_splitter=RecursiveCharacterTextSplitter(
              chunk_size=1000,
              chunk_overlap=200
          )
          chunks=text_splitter.split_text(texts)
          
          vector_db=FAISS.from_texts(chunks,emb)
          vector_db.save_local(DB_PATH)
          
          retriever=vector_db.similarity_search(query,k=4)
          return preref(text=retriever,question=query,temperature=temperature,model=model)
  else:
      return "Sorry but you have to provide query and DB_PATH also in order to retrieve from Vectorised DataBase"

  
#REFINE INITIALISATION
def preref(text,question, temperature, model, **kwargs):
  ref=refine(
      text=text,
      question=question,
      temperature=temperature,
      model=model
  )
  result=ref.refinef()
  return result


#REFINE
class refine:
  def __init__(self,text,question, temperature, model):
    self.text=text
    self.question=question
    self.temperature=temperature
    self.model=model

  def refinef(self):
    texts=self.text
    question=self.question
    temperature=self.temperature
    model=self.model
    answers=[]
    no=len(texts)
    no_of_loop=0
    for i in range(no):
      context=texts[i]
      prompt=f"""Use the following information to answer the question: 
      Text: {context}
      Existing Answer: {answers}
      Question: {question}
      """
      llm=Ollama(
          model=model,
          temperature=temperature
      )
      response=llm.invoke(prompt)
      time.sleep(3)
      if answers:
        answers.remove(answers[0])
        answers.append(response)
      else:
        answers.append(response)
      if not no_of_loop==no:
        no_of_loop+=1
      else:
        pass
    return response
