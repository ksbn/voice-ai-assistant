# 🎙️ Daniel AI - Next-Gen Voice Assistant

Daniel is a modern, ultra-low latency voice assistant web application powered by the **Groq API** and built with a FastAPI backend.

---

##  Features

* **⚡ Ultra-Fast LLM Inference**: Powered by Groq for instantaneous, conversational AI responses.
* **✨ Pro UI / UX Design**: Deep blue frosted glassmorphism interface featuring dynamic animated soundbar visualizers and responsive state transitions.
* **🗣️ Voice-First Interaction**: Built using the Web Speech API for seamless browser-based voice recognition and speech synthesis (text-to-speech).
* **🚀 Cloud-Ready (Vercel)**: Configured for smooth deployment on Vercel using a serverless FastAPI architecture.

---

##  Project Architecture

```text
├── index.html        # Frontend user interface (Dark Pro Glassmorphism design)
├── server.py         # FastAPI backend server (Handles routing and Groq API calls)
├── voiceassistant.py # Desktop client integration (Optional local runtime)
├── main.py           # Application entry point
├── vercel.json       # Vercel deployment configuration
└── requirements.txt  # Python package dependencies

🛠️ Tech Stack
Frontend: HTML5, Modern CSS3 (Grid, Custom Properties, Glassmorphism, Animations), Vanilla JavaScript (Web Speech API).
Backend: Python, FastAPI, Uvicorn, Pydantic.
AI Engine: Groq API Client (groq).
Hosting & Deployment: Vercel Serverless Functions.

