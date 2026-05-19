from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GroundwaterDataSchema(BaseModel):
    state: str
    district: str
    rainfall_mm: Optional[float] = None
    ground_water_recharge: Optional[float] = None
    gw_extraction: Optional[float] = None
    stage_of_gw_extraction: Optional[float] = None
    net_gw_availability: Optional[float] = None
    
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    data: Optional[List[dict]] = None
    suggestions: Optional[List[str]] = None
    chart_data: Optional[Dict[str, Any]] = None  # Added for charts
