from fastapi import APIRouter
from ..utils.prompt_builder import build_prompt
from ..utils.llm_client import call_llm

router = APIRouter(tags=["AI Explanation"])

@router.post("/financial-summary")
async def explain_finances(payload: dict):
    prompt = build_prompt(payload)
    explanation = await call_llm(prompt)
    return {"explanation": explanation}

