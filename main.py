import os
import sys

# =============================
# 🔹 BASE DIRECTORY
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# =============================
# 🔹 FASTAPI IMPORTS
# =============================
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# =============================
# 🔹 IMPORT ROUTES
# =============================
from routes import sentiment

# =============================
# 🔥 IMPORT DATABASE INIT
# =============================
from database.db import init_db

# =============================
# 🔹 CREATE APP
# =============================
app = FastAPI(
    title="AI Sentiment API",
    version="2.0"
)

# =============================
# 🔓 ENABLE CORS (IMPORTANT FOR FRONTEND)
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# 🔥 INIT DATABASE
# =============================
init_db()
print("✅ Database initialized")

# =============================
# 🔹 STATIC FILES
# =============================
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# =============================
# 🔹 TEMPLATES
# =============================
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

# =============================
# 🔹 ROUTERS
# =============================
app.include_router(
    sentiment.router,
    prefix="/api/sentiment",
    tags=["Sentiment"]
)

# =============================
# 🔹 HOME
# =============================
@app.get("/", response_class=JSONResponse)
def home():
    return {
        "status": "Backend running ✅",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }

# =============================
# 🔹 DASHBOARD
# =============================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

# =============================
# 🔹 HEALTH CHECK
# =============================
@app.get("/health")
def health():
    return {"status": "OK"}

# =============================
# 🔥 RUN SERVER + AUTO OPEN
# =============================
if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000/dashboard")

    print("🚀 STARTING SERVER...")

    threading.Thread(target=open_browser).start()

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )