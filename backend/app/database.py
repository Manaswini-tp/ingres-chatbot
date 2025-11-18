from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

Base = declarative_base()

class GroundwaterData(Base):
    __tablename__ = "groundwater_data"
    
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    year = Column(Integer, index=True)
    month = Column(String)
    groundwater_level = Column(Float)
    water_quality = Column(String)
    rainfall = Column(Float)
    category = Column(String)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/groundwater_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_mock_data():
    """Create mock groundwater data for demonstration"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(GroundwaterData).first():
            return
            
        states_districts = {
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Belgaum"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
            "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
            "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"]
        }
        
        data = []
        for state, districts in states_districts.items():
            for district in districts:
                for year in range(2018, 2025):
                    for month_idx, month in enumerate(["Jan", "Apr", "Jul", "Oct"]):
                        # Simulate realistic groundwater levels (in meters)
                        base_level = 8.0 + (year - 2018) * 0.5  # Gradual decline
                        seasonal_variation = [0.5, -1.0, -2.0, -0.5][month_idx]
                        rainfall_variation = [1200, 800, 600, 900][month_idx] + (year - 2018) * 50
                        
                        data.append({
                            "state": state,
                            "district": district,
                            "year": year,
                            "month": month,
                            "groundwater_level": max(2.0, base_level + seasonal_variation),
                            "rainfall": max(400, rainfall_variation),
                            "water_quality": ["Good", "Moderate", "Poor"][(hash(state + district) % 3)],
                            "category": ["Safe", "Semi-Critical", "Critical"][(hash(state + district + str(year)) % 3)]
                        })
        
        # Insert mock data
        for item in data:
            record = GroundwaterData(**item)
            db.add(record)
        
        db.commit()
        print("Mock data created successfully!")
        
    except Exception as e:
        print(f"Error creating mock data: {e}")
    finally:
        db.close()