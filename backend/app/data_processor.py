import pandas as pd
from sqlalchemy.orm import Session
from .models import GroundwaterData
from .database import engine, SessionLocal
import logging

logger = logging.getLogger(__name__)

def clean_numeric(value):
    """Convert value to float, return None if not possible"""
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (ValueError, TypeError):
        return None

def load_ingres_data_to_db(file_path: str = "ingres-data.xlsx"):
    """
    Load INGRES Excel data into PostgreSQL database with enhanced cleaning
    """
    try:
        logger.info(f"Loading data from {file_path}")
        
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name='GEC', skiprows=7)
        
        # Clean data
        df = df.dropna(subset=['STATE', 'DISTRICT'], how='all')
        df = df[df['STATE'].notna()]
        df = df[df['STATE'].astype(str).str.strip() != '']
        
        # Prepare data records
        records = []
        for _, row in df.iterrows():
            try:
                record = {
                    's_no': str(row.get('S.No', '')),
                    'state': str(row.get('STATE', '')).strip().upper(),
                    'district': str(row.get('DISTRICT', '')).strip().upper(),
                    'assessment_unit': str(row.get('ASSESSMENT UNIT', '')),
                    'rainfall_mm': clean_numeric(row.get('Rainfall (mm)')),
                    'total_geographical_area': clean_numeric(row.get('Total Geographical Area (ha)')),
                    'ground_water_recharge': clean_numeric(row.get('Ground Water Recharge (ham)')),
                    'annual_extractable_gw_resource': clean_numeric(row.get('Annual Extractable Ground water Resource (ham)')),
                    'gw_extraction': clean_numeric(row.get('Ground Water Extraction for all uses (ha.m)')),
                    'stage_of_gw_extraction': clean_numeric(row.get('Stage of Ground Water Extraction (%)')),
                    'net_gw_availability': clean_numeric(row.get('Net Annual Ground Water Availability for Future Use (ham)'))
                }
                
                if record['state'] and record['district']:
                    records.append(record)
            except Exception as e:
                logger.warning(f"Error processing row: {e}")
                continue
        
        # Load to database
        db = SessionLocal()
        try:
            # Clear existing data
            db.query(GroundwaterData).delete()
            
            # Insert new data
            for record in records:
                db_record = GroundwaterData(**record)
                db.add(db_record)
            
            db.commit()
            logger.info(f"Successfully loaded {len(records)} records into database")
            return len(records)
        except Exception as e:
            db.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
