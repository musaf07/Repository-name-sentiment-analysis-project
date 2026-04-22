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

# =============================
# 🔹 IMPORT ROUTES
# =============================
from routes import sentiment   # ✅ make sure this path is correct

# =============================
# 🔹 CREATE APP
# =============================
app = FastAPI(
    title="Sentiment API",
    version="1.0"
)

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
    prefix="/api/sentiment",   # ✅ IMPORTANT URL PREFIX
    tags=["Sentiment"]
)

# =============================
# 🔹 HOME
# =============================
@app.get("/", response_class=JSONResponse)
def home():
    return {
        "status": "Backend running ✅",
        "docs": "/docs",
        "test_api": "/api/sentiment/analyze"
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
# 🔥 RUN SERVER
# =============================
if __name__ == "__main__":
    import uvicorn

    print("🚀 STARTING SERVER...")

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False   # ❗ IMPORTANT: disable reload for now
    )