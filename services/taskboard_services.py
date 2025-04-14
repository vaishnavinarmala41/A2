from google.cloud import firestore
database = firestore.Client()



def get_user_taskboards(useremail):
    user_tasks = []
    taskboards_ref = database.collection("taskboards")
    taskboards = taskboards_ref.stream()
    # print("user email is ",useremail, taskboards)
    for taskboard in taskboards:
        taskboard_data = taskboard.to_dict()
        # board_id = taskboard.boardId
        # print("taskboard ",taskboard_data)
        if useremail == taskboard_data.get("admin") or useremail in taskboard_data.get("collaborators", []):
            # taskboard_data["board_id"] = board_id
            user_tasks.append(taskboard_data)
    print("user tasks ",user_tasks)
    return {"user_tasks": user_tasks}

def create_taskboard(taskboardData):
    try:
        taskboard_dict = taskboardData.dict()   
        database.collection("taskboards").document(taskboardData.boardId).set(taskboard_dict)
        return {"sucess":True}
    except Exception as e:
        return {"sucess":False}
    

def get_taskboard_using_boardID(boardID):
    doc_ref = database.collection("taskboards").document(boardID)
    doc = doc_ref.get()
    taskboard_data = None
    if doc.exists:
        taskboard_data = doc.to_dict()
    else:
        pass
    
    return {"taskboard_data": taskboard_data}

def search_name(name):
    try:
        does_board_exist = database.collection('taskboards').where('name', '==', name).limit(1).get()

        if does_board_exist:
            return {"found":True}
        else:
            return {"found":False}
    except Exception as e:
        # print("An error occurred:", e)
        return {"Error": e}
        




