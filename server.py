import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="Daniel Voice Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

chat_history = [
    {
        "role": "system",
        "content": "You are Daniel, a friendly, concise AI voice assistant. Keep answers brief (1-2 short sentences)."
    }
]

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error loading UI: {str(e)}</h3>", status_code=404)

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GROQ_API_KEY environment variable is missing."
        )

    user_text = request.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")

    chat_history.append({"role": "user", "content": user_text})

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=chat_history # type: ignore
        )
        ai_reply = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_reply}) # type: ignore
        return {"reply": ai_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")

@app.post("/api/reset")
def reset_conversation():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "You are Daniel, a friendly, concise AI voice assistant. Keep answers brief (1-2 short sentences)."
        }
    ]
    return {"status": "cleared"}