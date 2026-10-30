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

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
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