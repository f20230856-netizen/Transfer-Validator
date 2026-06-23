# nodes/verdict.py
from pydantic import BaseModel
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI

class VerdictModel(BaseModel):
    recommendation: Literal["Proceed", "Caution", "Avoid"]
    confidence: int
    reasoning: str
    key_factors: list[str]

VERDICT_SYS = (
    "You are a sporting director. Decide Proceed/Caution/Avoid using ONLY the "
    "structured data provided. You MAY NOT invent stats. Lower your confidence "
    "for every missing data source. Reference credibility, value premium, "
    "tactical fit, and World Cup hype risk explicitly."
)

def verdict_node(state: dict) -> dict:
    # Initialized inside the function so imports don't crash without an API key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    payload = {
        "credibility": state.get("credibility"),
        "performance": state.get("performance"),
        "value": state.get("value"),
        "fit": state.get("fit"),
        "errors": state.get("errors", []),
    }
    v = llm.with_structured_output(VerdictModel).invoke(
        f"{VERDICT_SYS}\n\nDATA:\n{payload}"
    )
    return {"verdict": v.model_dump()}