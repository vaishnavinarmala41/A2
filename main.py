from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from google.cloud import firestore
from services import taskboard_services as service
from uuid import uuid4
app = FastAPI()

# Serve static files like CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set template directory
templates = Jinja2Templates(directory="templates")


# Connect with database 
database = firestore.Client()

# models 
class EmailRequest(BaseModel):
    email: str



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
 
@app.get("/taskboards", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("taskboards.html", {"request": request})
 
 #Checks if user exist if not exist then creates one 
@app.post("/createnewuser")
async def create_user(data: EmailRequest):
    try:
        user_ref = database.collection('users').where('email', '==', data.email).limit(1).get()

        if not user_ref:
            user_id = str(uuid4())
            database.collection('users').add({
                "email": data.email,
                "userId": user_id
            })
            print("User added:", data.email)
        else:
            print("ℹUser already exists:")

    except Exception as e:
        print("Error:", e)
        return {"message": "Failed to add user", "error": str(e)}

    return {"message": "Processed user request"}



@app.get("/gettaskboards")
async def get_taskboards():
    try:
        service.display_task()
    except Exception as e:
        return {"Error":e}
