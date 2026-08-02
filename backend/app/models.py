from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from .database import Base

class GroundwaterData(Base):
    __tablename__ = "groundwater_data"
    
    id = Column(Integer, primary_key=True, index=True)
    s_no = Column(String, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    assessment_unit = Column(String)
    rainfall_mm = Column(Float)
    total_geographical_area = Column(Float)
    ground_water_recharge = Column(Float)
    annual_extractable_gw_resource = Column(Float)
    gw_extraction = Column(Float)
    stage_of_gw_extraction = Column(Float)
    net_gw_availability = Column(Float)
    
class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    language = Column(String, default="en")
    timestamp = Column(DateTime, default=datetime.utcnow)

from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    query_count = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
