from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import sqlite3

# --- SETUP ---
app = FastAPI()

# Important: Mount static and templates BEFORE the routes
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()
ADMIN_USERNAME = "oduro kelvin"
ADMIN_PASSWORD = "KelvinOduro544"

# --- DATABASE INIT ---
# This creates the file and table so the app doesn't crash
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, tier TEXT, 
                  daily_usage INTEGER, last_use_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- AUTH LOGIC ---
def check_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/prompts", response_class=HTMLResponse)
async def read_prompts_page(request: Request):
    return templates.TemplateResponse("prompts.html", {"request": request})

@app.get("/secret-admin-portal")
async def admin_dashboard(request: Request, authenticated: bool = Depends(check_admin)):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, tier, daily_usage, last_use_date FROM users")
    users = c.fetchall()
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
