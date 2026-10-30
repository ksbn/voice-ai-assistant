from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Daniel AI backend is online and ready!", "endpoint": "/chat (POST)"}

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    if not client:
        return {"error": "GROQ_API_KEY environment variable is missing on Vercel dashboard."}
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are Daniel, a friendly, concise AI assistant. Keep answers short."},
                {"role": "user", "content": request.prompt}
            ]
        )
        reply = completion.choices[0].message.content
        return {"response": reply}
    except Exception as e:
        return {"error": str(e)}