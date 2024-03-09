from fastapi import APIRouter
from models.note import Note
from config.db import conn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from schemas.note import noteEntity, notesEntity
from fastapi.templating import Jinja2Templates
note = APIRouter()
templates = Jinja2Templates(directory="templates")
from bson import ObjectId

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # This is for only for fetch one data
    # docs=conn.notes.notes.find_one({})
    # print(docs)

    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],

        })
        # print(new_docs)
        # print(type(doc)," doc")
        # print(type(docs)," docs")
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": new_docs})


@note.post("/", response_class=HTMLResponse)
async def create_item(request: Request):
    form = await request.form()
    form_dict = dict(form)
    form_dict["important"] = True if form_dict.get("important") == "on" else False
    message = ""
    try:
        note = conn.notes.notes.insert_one(form_dict)
        message = "Note successfully created"

    except Exception as e:
        error_message = f"Error: {str(e)}"
        message=error_message
        # return templates.TemplateResponse("index.html", {"request": request, "message": error_message,"newDocs": new_docs})
    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
        })
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "newDocs": new_docs})
@note.post("/delete/{note_id}", response_class=HTMLResponse)
async def delete_item(note_id: str, request: Request):
    print(note_id)
    message=""
    try:
        # Convert note_id to ObjectId
        note_object_id = ObjectId(note_id)
        # print(note_object_id)
        # Perform the deletion operation here, for example:
        myquery ={"_id": note_object_id}
        delete_stat = conn.notes.notes.delete_one(myquery)
        # print(delete_stat)
        # Return a success message after deletion
        message = "Note deleted successfully"
        # return templates.TemplateResponse("index.html", {"request": request, "message": message})
    except Exception as e:
        # Return an error message if deletion fails
        error_message = f"Error: {str(e)}"
        message=error_message

    docs= conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append(({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
        }))
    # print(message)
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "newDocs": new_docs})
@note.post("/update/{note_id}",response_class=HTMLResponse)
async def update_item(note_id:str,request:Request):
    note_object_id=ObjectId(note_id)
    docs = conn.notes.notes.find({"_id":note_object_id})
    print(docs," ", type(docs))
    nodeList = []
    for doc in docs:
        nodeList.append(doc)
    # print(nodeList)

    return templates.TemplateResponse("updateNote.html",{"request":request,"nodeList":nodeList})



@note.post("/submit_update", response_class=HTMLResponse)
async def finalUpdate(request: Request):
    form = await request.form()
    form_dict = dict(form)
    print(form_dict)
    form_dict["important"] = True if form_dict.get("important") == "on" else False
    message = ""
    try:
        # Convert _id string to ObjectId
        note_object_id = ObjectId(form_dict.pop("_id"))

        # Update the note with the given note_id, excluding the _id field
        update_result = conn.notes.notes.update_one({"_id": note_object_id}, {"$set": form_dict})
        if update_result.modified_count == 1:
            message = "Note updated successfully"
        else:
            message = "Note not found or not updated"
    except Exception as e:
        # Return an error message if update fails
        error_message = f"Error: {str(e)}"
        message = error_message

    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
        })
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "newDocs": new_docs})
