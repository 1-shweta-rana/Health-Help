import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()

# --- Database Setup (Updated for Chat History) ---
DATABASE_URL = "sqlite:///./symptom_checker.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ChatTurn(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

# --- FastAPI App ---
app = FastAPI(title="Healthcare Symptom Checker Chatbot Backend")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Chat ---
class ChatPart(BaseModel):
    text: str

class ChatMessage(BaseModel):
    role: str
    parts: List[ChatPart]

class ChatInput(BaseModel):
    history: List[ChatMessage] = Field(..., description="The entire conversation history.")

# --- API Endpoint ---
@app.post("/chat")
async def chat_with_bot(data: ChatInput):
    db = SessionLocal()
    try:
        system_prompt = """You are a compassionate and helpful "Symptom Checker Bot". Your primary role is to engage in a conversation with a user to understand their symptoms before providing educational insights.

        Your conversation flow MUST be as follows:
        1.  Start by greeting the user and asking for their primary symptom. (This is handled by the frontend, but you should continue the conversation naturally).
        2.  Analyze the user's response. If the information is too vague or incomplete, you MUST ask ONE clarifying follow-up question. Examples: "How long have you had this symptom?", "Can you describe the pain on a scale of 1 to 10?", "Do you have a fever? If so, what is your temperature?".
        3.  Continue asking one simple question at a time until you have sufficient detail (e.g., symptom, duration, severity, related symptoms).
        4.  Once you feel you have enough information, and ONLY THEN, provide the final analysis in the specified format. You should explicitly state that you are now providing the summary.
        5.  The final analysis MUST be structured with markdown headings for "Possible Conditions", "Recommended Next Steps", and the "Important Disclaimer". It should be concise (200-250 words) and prioritize common, less severe conditions.
        6.  Rather than big paragraphs, give points and bolden the most probable outcome and be humanly in responses.
        7.  Remember its for INDIAN REGION 
        Keep your questions clear, simple, and empathetic. Do not overwhelm the user. Your goal is to guide the conversation naturally towards a helpful conclusion. and dont give big paragraphs keep it minimal and enough"""

        # ** THE FIX IS HERE **
        # Convert the list of Pydantic ChatMessage objects to a list of dictionaries
        history_as_dicts = [message.model_dump() for message in data.history]

        payload = {
            "contents": history_as_dicts, # Use the converted list
            "systemInstruction": {"parts": [{"text": system_prompt}]},
        }

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in .env file")
        
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(api_url, json=payload, headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error from AI API: {response.text}")

        result_json = response.json()
        candidate = result_json.get("candidates", [{}])[0]
        bot_output = candidate.get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I had trouble processing that. Could you try again?")

        last_user_message = data.history[-1].parts[0].text
        history_entry = ChatTurn(user_message=last_user_message, bot_response=bot_output)
        db.add(history_entry)
        db.commit()

        return {"reply": bot_output}

    except Exception as e:
        db.rollback()
        # Be more specific about the error type for better debugging
        if isinstance(e, httpx.RequestError):
             raise HTTPException(status_code=503, detail=f"Error connecting to AI service: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Symptom Checker Chatbot API is running. POST to /chat to start a conversation."}

