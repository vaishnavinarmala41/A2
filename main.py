from fastapi import FastAPI, Request , Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from google.cloud import firestore
from services import taskboard_services as service
from uuid import uuid4
from typing import List, Optional
from fastapi import HTTPException , status ,APIRouter
from fastapi.responses import JSONResponse
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

class BoardName(BaseModel):
    name:str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
 
@app.get("/taskboards", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("taskboards.html", {"request": request})

@app.get("/test2", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("test2.html", {"request": request})
 
@app.get("/test3", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("test3.html", {"request": request})
 
@app.get("/viewtaskboard/{boardID}", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("viewtaskboard.html", {"request": request})
 
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
        userTaskboards =  service.get_user_taskboards(useremail)
        return {"usertasks":userTaskboards}
    except Exception as e:
        return {"Error":e}


@app.post("/taskboard/submit")
async def create_taskboard(taskboardData: Taskboard):
    try:
        print("taskboard details ", taskboardData)
        
        taskboard_name_search = service.search_name(taskboardData.name)
        if taskboard_name_search['found']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task board already exists"
            )
        
        taskboard_creation = service.create_taskboard(taskboardData) 
        return JSONResponse(
            content={"message": "TaskBoard created"},
            status_code=status.HTTP_200_OK
        )

    except HTTPException as http_exc:
        raise http_exc  # Already includes status and message

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"message": "Failed to create task board", "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@app.get("/gettaskboardusingid/{boardId}")
async def get_taskboards(boardId):
    try:
        print("board id is ", boardId)
        taskboard =  service.get_taskboard_using_boardID(boardId)
        return {"taskboard":taskboard}
    except Exception as e:
        return {"Error":e}

#fetch all the users
@app.get("/getallusers")
async def get_all_users(request:Request):
    users_ref = database.collection("users")
    users = [doc.to_dict() for doc in users_ref.stream()]
    print("users inside main ",users)
    return {"users": users}


#update
@app.put("/updateTaskboard/{boardId}")
async def edit_taskboard(taskboard: Taskboard,boardId):
    print("updating task baord")
    taskboard_update = service.update_taskboard(taskboard,boardId) 
    print("updated")
    return {"board_updated":True}


#Verify board name
@app.post("/verifyBoardNameExist")
async def verify_taskboard_name(name: BoardName):
    print("updating task baord ",name)
    taskboard_name = service.verify_taskboard_name(name) 
    return {"boardNameExist":taskboard_name}