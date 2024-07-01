from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

# Ensure that Chat is imported if it's defined in the models module
from .models import Chat, User

def create_chat(db: Session, user_id: int):
    today_iso = date.today().isoformat()  # Get today's date in ISO format
    db_chat = Chat(user_id=user_id, date=today_iso)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_chat(db: Session, user_id: int):
    db_chat = Chat(user_id=user_id, date=date.today().isoformat())  # Converting date to string here
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).all()

def get_chats(db: Session, user_id: int):
    return db.query(models.Chat).filter(models.Chat.user_id == user_id).all()

def get_prompt(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id, models.Message.role == 'Bloom').order_by(models.Message.message_id.desc()).first()
