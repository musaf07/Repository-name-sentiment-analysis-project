from fastapi import APIRouter
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@router.post("/chat")
async def chat(data: dict):
    message = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant inside a sentiment dashboard."},
            {"role": "user", "content": message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }