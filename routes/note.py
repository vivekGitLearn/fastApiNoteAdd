from fastapi import APIRouter
from models.note import Note
from config.db import conn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from schemas.note import noteEntity, notesEntity
from fastapi.templating import Jinja2Templates

note = APIRouter()
templates = Jinja2Templates(directory="templates")


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
            "important": doc["important"]
        })
        print(new_docs)
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": new_docs})


@note.post("/",response_class=HTMLResponse)
async def create_item(request: Request):
   form=await request.form()
   print(form)
   formDict = dict(form)
   formDict["important"] = True if formDict["important"] =="on" else False
   note= conn.notes.notes.insert_one(dict(form))
   return {"Success": True}

