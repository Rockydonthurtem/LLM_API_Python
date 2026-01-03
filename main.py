from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os

from dotenv import load_dotenv

app = FastAPI()

API_KEYS_CREDIT = {os.getenv("API_KEY"): 2}

@app.post("/generate")

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEYS_CREDIT.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key or not credits")
    
    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEYS_CREDIT[x_api_key] -= 1
    response = ollama.chat(model="mistral", messages=[{"role": "users", "content": "prompt"}])
    return {"response": response["message"]["content"]}