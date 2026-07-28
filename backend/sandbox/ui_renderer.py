import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="yAI Generative UI Preview Engine")

# Security Hardening: Only allow localhost for previews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# In-memory store for generated components
# In production, this would be tied to session IDs, but this works for POC.
class ComponentStore:
    latest_html: str = """
    <html>
        <head><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-gray-900 text-white flex items-center justify-center h-screen">
            <h1 class="text-3xl font-bold">Waiting for yAI to generate a UI...</h1>
        </body>
    </html>
    """

class UIRenderRequest(BaseModel):
    html_content: str

@app.post("/render")
async def render_ui(request: UIRenderRequest):
    """
    Receives generated raw HTML/Tailwind/React code from the yAI Swarm 
    and instantly stages it for live preview.
    """
    # Ensure Tailwind is injected if not present for instant styling
    content = request.html_content
    if "tailwindcss.com" not in content and "<html" in content.lower():
        content = content.replace("</head>", '<script src="https://cdn.tailwindcss.com"></script></head>')
        
    ComponentStore.latest_html = content
    return {"status": "success", "preview_url": "http://127.0.0.1:8001/preview"}

@app.get("/preview", response_class=HTMLResponse)
async def get_preview():
    """
    Serves the latest compiled component instantly in the browser.
    """
    return HTMLResponse(content=ComponentStore.latest_html, status_code=200)

if __name__ == "__main__":
    print("[yAI Generative UI] Booting Zero-Latency Preview Engine on port 8001...")
    uvicorn.run("ui_renderer:app", host="127.0.0.1", port=8001, reload=False)
