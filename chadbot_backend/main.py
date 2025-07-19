from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import pathlib
import json
import difflib
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import cosine

app = FastAPI()

# Allow CORS for all origins for simplicity (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the frontend directory at /static
frontend_path = pathlib.Path(__file__).parent.parent / "chadbot_frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path), html=True), name="static")

# Load chatbot Q&A data from JSON file
data_file = pathlib.Path(__file__).parent / "chatbot_data.json"
with open(data_file, "r", encoding="utf-8") as f:
    chatbot_data = json.load(f)

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for questions
questions = [item["question"] for item in chatbot_data]
question_embeddings = model.encode(questions)

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
    user_question = msg.message

    # Compute embedding for user question
    user_embedding = model.encode([user_question])[0]

    # Find closest question by cosine similarity
    similarities = [1 - cosine(user_embedding, q_emb) for q_emb in question_embeddings]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    # Threshold for similarity
    if best_score > 0.5:
        answer = chatbot_data[best_idx]["answer"]
        return {"response": answer}

    # If no good match, return default message
    return {"response": "Sorry, I can only answer questions related to Tech Kshetra from my database. Please ask something else."}
