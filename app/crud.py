from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
import pytz

# Ensure that Chat is imported if it's defined in the models module
from .models import Chat, User

def create_user(db: Session, name: str):
    db_user = User(name=name)  # Converting date to string here
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_chat(db: Session, user_id: int):
    gmt_plus_8 = pytz.timezone('Asia/Singapore')  # Singapore is one of the regions on GMT+8
    db_chat = Chat(user_id=user_id, date=datetime.now(gmt_plus_8).date().today().isoformat())  # Converting date to string here
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def update_chat(db: Session, chat_id: int, chat: schemas.ChatUpdate):
    db_chat = db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    db_chat.mood = chat['mood']
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

def get_user(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()