from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, create_engine, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    chats = relationship("Chat", back_populates="user")

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    date = Column(String)  # Changed from Date to String
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    content = Column(Text)
    role = Column(String)
    chat = relationship("Chat", back_populates="messages")
