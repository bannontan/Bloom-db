from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_vertexai import ChatVertexAI
import os
import requests
import urllib
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_openai import ChatOpenAI
from numpy.linalg import norm
from .database import SessionLocal, SessionLocal2
from .models import Emotion
from sqlalchemy.orm import Session
import json
import ast
import re
from .crud import create_message, update_chat
from .models import Message, Chat
from .schemas import MessageCreate

os.environ["OPENAI_API_KEY"] = "<BLANK>"

def find_mood(text: str):
    # Pattern to find the specified words
    pattern = r'\b(joy|anger|fear|anticipation|sadness)\b'
    
    # Using findall to get all occurrences of the pattern
    found_word = re.search(pattern, text, re.IGNORECASE)
    
    return found_word.group(0) if found_word else None

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def find_similar_embeddings(input_vector, top_n=1):
    db = SessionLocal2()
    try:
        emotions = db.query(Emotion).all()
        similarities = []
        for emotion in emotions:
            try:
                db_vector = ast.literal_eval(emotion.embeddings)  # Convert string representation to list
            except (ValueError, SyntaxError) as e:
                continue  # Skip this entry if conversion fails
            similarity = cosine_similarity(input_vector, db_vector)
            similarities.append((emotion.emotion, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similarities = similarities[:top_n]
        return top_similarities
    finally:
        db.close()

def find_most_similar_embedding(input_vector):
    db = SessionLocal2()
    try:
        emotions = db.query(Emotion).all()
        best_similarity = -1
        best_emotion = None
        for emotion in emotions:
            
            try:
                db_vector = ast.literal_eval(emotion.embeddings)  # Convert string representation to list
            except (ValueError, SyntaxError) as e:
                continue  # Skip this entry if conversion fails
            similarity = cosine_similarity(input_vector, db_vector)
            if similarity > best_similarity:
                best_similarity = similarity
                best_emotion = emotion.emotion
        return best_emotion, best_similarity
    finally:
        db.close()

@tool
def sentiment_analysis(message: str) -> bytes:
    """This tool performs sentiment analysis on the input message. It will return the best emotion based on the pre-trained SBERT model. The best emotion identified will be used by the LLM to create a short summary of why the person feels this emotion from the input message. 
        The response should be conversational and engaging to the user. Be informal and friendly.

    Args:
        message (str): _description_

    Returns:
        bytes: _description_
    """
    # Load pre-trained SBERT model
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    input_vector = sbert_model.encode(message)
    best_emotion, best_similarity = find_most_similar_embedding(input_vector)

    return {'emotion': best_emotion} #Returns the result in JSON format (bytes)

def query_model(query:str) -> str:
    """
    Call this function from outside the module
    """
    model = ChatOpenAI(model="gpt-3.5-turbo")
    system_message = "Be informal and respond in a friendly manner. Engage the user in a conversation. Explain why the user feels this way by extracting information from the input. It should help the user have a better understanding of why they feel a certain way. The only emotions you should output are: 'Joy, Sadness, Anger, Fear, Anticipation'."
    tools = [sentiment_analysis]
    graph = create_react_agent(model, tools=tools, messages_modifier=system_message)
    
    prompt = f"Extract the emotion then summarize and explain why I feel this way from the text: {query}"
    
    inputs = {"messages": [
        ("user", prompt)
        ]}
    
    response = graph.invoke(inputs, stream_mode="updates") #Stream mode set to updates instead of values for less verbosity

    return response[-1]['agent']['messages'][-1].content #some nonsense to get to the actual text you want. Can implement StrOutputParser in the future to make it neater
    

def create_message_api(chat_id: int, content: str, role: str = "LLM"):
    db = SessionLocal()
    
    params = MessageCreate(content=content, role="User", chat_id=chat_id)
    
    create_message(db=db, message=params)

    output = query_model(content)
    mood = find_mood(output)

    params = MessageCreate(chat_id=chat_id, content=output, role=role)

    create_message(db=db, message=params)
    
    mood = find_mood(output)

    params = {'mood': mood}
    update_chat(db=db, chat_id=chat_id, chat=params)
        

if __name__ == '__main__':
    print(find_mood(query_model("I went for a run today and it felt great! I saw a cute dog on the way and it made my day. Towards the end of the run, I bumped into a close childhood friend and we went to have a meal together afterwards. Allowing us to catch up on each other's lives. It was a great day!")))
    