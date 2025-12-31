import google.generativeai as genai
from ..utils.config import settings

genai.configure(api_key=settings.GEMINI_AI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
    "You are a financial explanation engine embedded in a fintech app. "
    "You explain financial data in clean, well-written paragraphs. "
    "You NEVER use bullet points, lists, markdown, asterisks, or headings. "
    "You NEVER give advice or recommendations. "
    "You NEVER invent or assume numbers. "
    "Your tone is professional, neutral, and explanatory."
)
)

async def call_llm(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()