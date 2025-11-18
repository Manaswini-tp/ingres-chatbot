from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class QueryType(str, Enum):
    GROUNDWATER_LEVEL = "groundwater_level"
    WATER_QUALITY = "water_quality"
    TRENDS = "trends"
    COMPARISON = "comparison"

class ChatQuery(BaseModel):
    message: str
    language: str = "en"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    text: str
    chart_data: Optional[Dict[str, Any]] = None
    chart_type: Optional[str] = None
    raw_data: Optional[List[Dict]] = None
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "hi"