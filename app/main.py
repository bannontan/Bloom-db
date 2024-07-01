from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud, models, schemas
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/chats/", response_model=schemas.Chat)
def create_chat_api(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db=db, user_id=chat.user_id)

@app.post("/messages/", response_model=schemas.Message)
def create_message_api(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

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
