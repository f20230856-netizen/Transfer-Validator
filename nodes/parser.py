# nodes/parser.py
import os
from pydantic import BaseModel
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

class RumorClaimModel(BaseModel):
    player_name: str
    buying_club: str
    selling_club: Optional[str] = None
    reported_fee_eur: Optional[float] = None
    reported_source: Optional[str] = None
    report_date: Optional[str] = None

PARSE_SYS = (
    "Extract transfer rumor fields. Convert any fee to EUR (numeric). "
    "If a field is absent, return null. Do not invent sources."
)

def parser_node(state: dict) -> dict:
    # Initialized inside the function so imports don't crash without an API key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    text = state["rumor"]["raw_text"]
    parsed = llm.with_structured_output(RumorClaimModel).invoke(
        f"{PARSE_SYS}\n\nRUMOR: {text}"
    )
    claim = {**parsed.model_dump(), "raw_text": text}
    return {"rumor": claim}