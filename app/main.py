from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, SessionLocal2, engine2
from . import crud, models, schemas
from datetime import date
from . import lc
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine2)

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8000"
#     "http://localhost:8080",
#     "http://localhost:8001",
#     "https://bloom-sandy.vercel.app"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=user.name)

@app.post("/chats/", response_model=schemas.Chat)
def create_chat_api(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db=db, user_id=chat.user_id)

@app.post("/messages/", response_model=schemas.Message)
def create_message_api(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.patch("/chats/{chat_id}", response_model=schemas.Chat)
def update_chat_api(chat_id: int, chat: schemas.ChatUpdate, db: Session = Depends(get_db)):
    return crud.update_chat(db=db, chat_id=chat_id, chat=chat)

@app.get("/users/{name}", response_model=schemas.User)
def get_user(name: str, db: Session = Depends(get_db)):
    return crud.get_user(db=db, name=name)

@app.get("/messages/{chat_id}", response_model=list[schemas.Message])
def read_messages(chat_id: int, db: Session = Depends(get_db)):
    return crud.get_messages(db=db, chat_id=chat_id)

@app.get("/chats/{user_id}", response_model=list[schemas.Chat])
def read_chats(user_id: int, db: Session = Depends(get_db)):
    return crud.get_chats(db=db, user_id=user_id)

@app.get("/prompt/{chat_id}", response_model=schemas.Message)
def read_prompt(chat_id: int, db: Session = Depends(get_db)):
    prompt = crud.get_prompt(db=db, chat_id=chat_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@app.post("/langchain/")
def langchain_endpoint(user_input: schemas.MessageCreate, db: Session = Depends(get_db)):
    try:
        user_message = user_input.content
        lc.create_message_api(user_input.chat_id, user_message, role = 'LLM') 
        return {"message": "Message created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))