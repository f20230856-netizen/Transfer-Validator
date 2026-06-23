# state.py
from typing import TypedDict, List, Optional, Annotated
import operator

class RumorMetadata(TypedDict):
    player_name: Optional[str]
    buying_club: Optional[str]
    selling_club: Optional[str]
    reported_fee_eur: Optional[int]
    reported_source: Optional[str]
    report_date: Optional[str]
    raw_text: str

class GraphState(TypedDict):
    rumor: RumorMetadata
    credibility: dict
    performance: dict
    value: dict
    fit: dict
    verdict: dict
    errors: Annotated[List[str], operator.add]