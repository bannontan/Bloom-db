from pydantic import BaseModel, validator, ValidationError
from datetime import date
from typing import Optional

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    chat_id: int

class Message(MessageBase):
    message_id: int
    chat_id: int

    class Config:
        orm_mode = True

# class ChatBase(BaseModel):
#     date: str

class ChatCreate(BaseModel):
    user_id: int

class Chat(BaseModel):
    chat_id: int
    user_id: int
    date: str  # This will be set automatically, no input required
    mood: str
    
    class Config:
        orm_mode = True

class ChatUpdate(BaseModel):
    mood: str
        
class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    chats: list[Chat] = []

    class Config:
        orm_mode = True

class Emotion(BaseModel):
    emotion: str
    embeddings: list[float]

    class Config:
        orm_mode = True
