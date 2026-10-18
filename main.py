from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import ollama
import os

app = FastAPI(title="Daniel Voice Assistant API")

chat_history = [
    {
        "role": "system",
        "content": "You are Daniel, a friendly, concise AI voice assistant. Keep answers brief (1-2 short sentences) so they are easy and natural to hear."
    }
]

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/chat")
async def chat(request: ChatRequest):
    user_text = request.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")

    chat_history.append({"role": "user", "content": user_text})

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=chat_history
        )
        ai_reply = response["message"]["content"]
        chat_history.append({"role": "assistant", "content": ai_reply})
        return {"reply": ai_reply}
    except Exception as e:
        print(f"Ollama Error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with local AI engine.")

@app.post("/api/reset")
async def reset_conversation():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "You are Daniel, a friendly, concise AI voice assistant. Keep answers brief (1-2 short sentences) so they are easy and natural to hear."
        }
    ]
    return {"status": "cleared"}