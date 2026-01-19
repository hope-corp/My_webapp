
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import sqlite3
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# 1. SET YOUR SECRET CREDENTIALS HERE
ADMIN_USERNAME = "your_name"
ADMIN_PASSWORD = "your_secret_password"

def check_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

# 2. THE SECRET ADMIN URL
@app.get("/secret-admin-portal") # Change this to anything hard to guess!
async def admin_dashboard(request: Request, authenticated: bool = Depends(check_admin)):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, tier, daily_usage, last_use_date FROM users")
    users = c.fetchall()
    conn.close()
    
    # Return a template with the user data
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})


app = FastAPI()

# Mount the 'static' folder for CSS and Images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point to the 'templates' folder for HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This sends index.html to the user's browser
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
