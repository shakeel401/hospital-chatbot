from fastapi import APIRouter, HTTPException
from app.services.chatbot import run_chatbot

router = APIRouter()

@router.post("/chat")
async def chat(data: dict):
    try:
        user_input = data.get("user_input", "").strip()
        thread_id = data.get("thread_id", "").strip()

        if not user_input:
            raise HTTPException(status_code=400, detail="User input is required")

        chatbot_response = run_chatbot(user_input, thread_id)

        if not chatbot_response:
            raise HTTPException(status_code=500, detail="Chatbot response is empty")

        return chatbot_response  # Ensure JSON is always returned

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
