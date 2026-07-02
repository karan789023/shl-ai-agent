from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import traceback

from app.agent import AIAgent
from services.retriever import load_catalog

router = APIRouter(tags=["Chat"])

# ---------- Load Catalog ----------

catalog = []
try:
    catalog = load_catalog()
    print(f"Catalog loaded successfully ({len(catalog)} assessments)")
except Exception:
    print("========== CATALOG LOAD ERROR ==========")
    traceback.print_exc()
    print("========================================")

# ---------- Init Agent ----------

agent = None

try:
    api_key = os.getenv("GEMINI_API_KEY")

    print("API KEY FOUND:", api_key is not None)

    agent = AIAgent(
        catalog=catalog,
        api_key=api_key
    )

    print("AI Agent initialized successfully")

except Exception:
    print("========== AGENT INIT ERROR ==========")
    traceback.print_exc()
    print("======================================")
    agent = None

# ---------- Request ----------

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]


# ---------- Response ----------

class ChatResponse(BaseModel):
    reply: str
    recommendations: list = []
    end_of_conversation: bool = False


# ---------- Chat Endpoint ----------

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:

        if agent is None:
            raise HTTPException(
                status_code=500,
                detail="AI Agent not initialized"
            )

        if not request.messages:
            raise HTTPException(
                status_code=400,
                detail="messages cannot be empty"
            )

        last_message = request.messages[-1]

        query = (
            last_message.get("content")
            or last_message.get("message")
        )

        if not query:
            raise HTTPException(
                status_code=400,
                detail="Invalid message format"
            )

        print(f"\nUser Query: {query}")

        result = agent.run(query)

        print("Agent executed successfully")

        return ChatResponse(
            reply=result.get("response", ""),
            recommendations=result.get("results", []),
            end_of_conversation=False
        )

    except HTTPException:
        raise

    except Exception:
        print("\n========== CHAT ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )