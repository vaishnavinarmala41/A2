from fastapi import FastAPI, Request , Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from google.cloud import firestore
from services import taskboard_services as service
from uuid import uuid4
from typing import List, Optional

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

class Task(BaseModel):
    name: str
    users: List[str] 
    status: str  
    pendingDate: str
    finishedDate:str

class Taskboard(BaseModel):
    boardId:str
    name:str
    admin:str
    tasks:Optional[List[Task]] = []
    collaborators:List[str]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
 
@app.get("/taskboards", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("taskboards.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})
 
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
            # print("User added:", data.email)
        else:
            # print("ℹUser already exists:")
            pass

    except Exception as e:
        print("Error:", e)
        return {"message": "Failed to add user", "error": str(e)}

    return {"message": "Processed user request"}


@app.get("/gettaskboards/{useremail}")
async def get_taskboards(useremail):
    try:
        print("email is ",useremail)
        userTaskboards =  service.display_task(useremail)
        return {"usertasks":userTaskboards}
    except Exception as e:
        return {"Error":e}


@app.post("/taskboard/submit")
async def create_taskboard(taskboardData: Taskboard):
    try:
        print("taskboard detaisl ",taskboardData)
        return {"message": "TaskBoard created"}
    except Exception as e:
        print("Error:", e)
        return {"message": "Failed to add user", "error": str(e)}


