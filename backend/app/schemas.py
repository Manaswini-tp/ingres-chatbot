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

from datetime import datetime

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: str
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    query_count: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Schema for token data"""
    email: Optional[str] = None
