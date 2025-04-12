from google.cloud import firestore
database = firestore.Client()



def display_task(useremail):
    user_tasks = []
    taskboards_ref = database.collection("taskboards")
    taskboards = taskboards_ref.stream()

    for taskboard in taskboards:
        taskboard_data = taskboard.to_dict()
        board_id = taskboard.id

        if useremail == taskboard_data.get("createdBy") or useremail in taskboard_data.get("members", []):
            taskboard_data["board_id"] = board_id
            user_tasks.append(taskboard_data)

    return {"user_tasks": user_tasks}

