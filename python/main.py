from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .chatbot import get_reply

# aboutme/ folder (the parent of the "python" folder)
SITE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Aboutme Chatbot API", version="1.0.0")

# Only needed if you open the site from another server (e.g. Live Server).
# When FastAPI serves the site itself, requests are same-origin and this is unused.
allow_origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://mohammadreza08080-arch.github.io/MRX",
]



class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class ChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    confidence: float


# ---------- API ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# "def" (not "async def") on purpose: model.predict is blocking,
# so FastAPI runs it in a thread pool instead of freezing the server.
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply, intent, confidence = get_reply(req.message.strip())
    return ChatResponse(reply=reply, intent=intent, confidence=round(confidence, 4))


# ---------- Website ----------
@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def home():
    return FileResponse(SITE_DIR / "index.html")


# Mount only the public site folders (never the whole aboutme/ folder:
# it contains env/, model/, pkl/ and your Python source).
# Must come AFTER the API routes above. Add your own folder names if needed.
for folder in ("html", "css", "js", "images", "img", "assets", "fonts"):
    folder_path = SITE_DIR / folder
    if folder_path.is_dir():
        app.mount(f"/{folder}", StaticFiles(directory=folder_path), name=folder)
