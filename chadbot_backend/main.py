from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow CORS for all origins for simplicity (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy chatbot Q&A data
chatbot_data = [
    {"question": "What is Tech Kshetra?", "answer": "Tech Kshetra is a platform for technology enthusiasts to learn and share knowledge."},
    {"question": "How can I join Tech Kshetra?", "answer": "You can join by signing up on our website and participating in our community events."},
    {"question": "What services does Tech Kshetra offer?", "answer": "We offer tutorials, workshops, and a community forum for tech discussions."}
]

# In-memory storage for chat messages (dummy)
chat_messages = []

class ChatMessage(BaseModel):
    user: str
    message: str

@app.get("/chatbot/info")
async def get_chatbot_info():
    return {"chatbot_name": "Chadbot AI Assistant", "data": chatbot_data}

@app.post("/chatbot/message")
async def post_chat_message(msg: ChatMessage):
    chat_messages.append(msg.dict())
    user_question = msg.message.lower()

    # Check for direct match in chatbot_data (case-insensitive)
    for item in chatbot_data:
        if item["question"].lower() == user_question:
            return {"response": item["answer"]}

    # If no direct match, return a default message encouraging to ask known questions
    return {"response": "Sorry, I can only answer questions related to Tech Kshetra from my database. Please ask something else."}
