from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from . import models, schemas, crud
from .database import engine, get_db
from .translation import translator
import logging
import httpx
import os  # ADD THIS

# ========== ADD THESE NEW IMPORTS ==========
from . import auth
from .models import User
from .schemas import UserCreate, UserLogin, Token, UserResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="INGRES Chatbot API", version="3.0")

# CORS - Update this with your Vercel URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rasa configuration
RASA_SERVER_URL = "http://localhost:5005"
USE_RASA = True

# ========== MODIFY STARTUP EVENT (Remove Excel Loading) ==========
@app.on_event("startup")
async def startup_event():
    """Check database connection on startup"""
    from .database import SessionLocal
    from .models import GroundwaterData
    
    db = SessionLocal()
    try:
        count = db.query(GroundwaterData).count()
        if count == 0:
            logger.warning("⚠️ Database is empty! Please run seed script.")
        else:
            logger.info(f"✅ Database ready with {count} records")
    except Exception as e:
        logger.error(f"✗ Database connection error: {e}")
    finally:
        db.close()
    
    # Check Rasa availability
    global USE_RASA
    if USE_RASA:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{RASA_SERVER_URL}/status")
                if response.status_code == 200:
                    logger.info("✓ Rasa server is available")
                else:
                    logger.warning("⚠ Rasa server not responding, using pattern matching")
                    USE_RASA = False
        except:
            logger.warning("⚠ Rasa server not available, using pattern matching")
            USE_RASA = False

# ========== REST OF YOUR EXISTING CODE (keep your functions) ==========
# Keep: normalize_location_name, get_rasa_prediction, extract_locations_from_text

# ========== ADD AUTH ROUTES ==========

@app.post("/api/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # Create user
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    db_user = auth.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    db_user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "full_name": db_user.full_name,
            "created_at": db_user.created_at,
            "query_count": db_user.query_count
        }
    }

@app.post("/api/logout")
def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Logged out successfully"}

@app.get("/api/me", response_model=UserResponse)
def get_me(token: str, db: Session = Depends(get_db)):
    """Get current user from token"""
    user = auth.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# ========== MODIFY YOUR CHAT ENDPOINT ==========
@app.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    message: schemas.ChatMessage,
    token: Optional[str] = None,  # ADD THIS
    db: Session = Depends(get_db)
):
    try:
        # Track user queries if authenticated
        if token:
            user = auth.get_current_user(db, token)
            if user:
                user.query_count += 1
                db.commit()
        
        # ========== REST OF YOUR CHAT LOGIC (KEEP AS IS) ==========
        user_message = message.message.strip()
        user_language = message.language
        
        logger.info(f"{'='*60}")
        logger.info(f"Query: '{user_message}' | Language: '{user_language}'")
        
        # Detect language
        if user_language == "auto" or not user_language:
            user_language = translator.detect_language(user_message)
            logger.info(f"Detected language: {user_language}")
        
        # Translate to English
        english_message = user_message.lower()
        if user_language != 'en':
            try:
                english_message = translator.translate_text(user_message, 'en', user_language).lower()
                logger.info(f"Translated: '{english_message}'")
            except Exception as e:
                logger.error(f"Translation error: {e}")
                english_message = user_message.lower()
        
        # Get Rasa prediction
        rasa_data = await get_rasa_prediction(english_message)
        rasa_intent = None
        rasa_confidence = 0.0
        rasa_entities = []
        
        if rasa_data:
            rasa_intent = rasa_data.get('intent', {}).get('name')
            rasa_confidence = rasa_data.get('intent', {}).get('confidence', 0.0)
            rasa_entities = rasa_data.get('entities', [])
            logger.info(f"Rasa: intent={rasa_intent} (conf={rasa_confidence:.2f}), entities={rasa_entities}")
        
        # Build location maps
        states = crud.get_all_states(db)
        all_data = db.query(models.GroundwaterData).all()
        
        district_map = {}
        state_map = {}
        
        for data in all_data:
            if data.district:
                district_variations = normalize_location_name(data.district)
                for variant in district_variations:
                    district_map[variant] = (data.district, data.state)
            
            if data.state:
                state_lower = data.state.lower()
                state_map[state_lower] = data.state
        
        bot_response = ""
        data_results = []
        suggestions = []
        chart_data = None
        
        search_text = f"{user_message.lower()} {english_message}"
        
        # Extract locations from text and Rasa entities
        locations = extract_locations_from_text(search_text, states, district_map)
        
        # Add Rasa entities
        for entity in rasa_entities:
            entity_value = entity.get('value', '').lower()
            entity_type = entity.get('entity', '')
            
            if entity_type in ['state', 'location']:
                for state in states:
                    if state.lower() in entity_value or entity_value in state.lower():
                        if state not in locations['states']:
                            locations['states'].append(state)
            
            if entity_type in ['district', 'location']:
                for dist_key, (dist_val, state_val) in district_map.items():
                    if dist_key in entity_value or entity_value in dist_key:
                        if dist_val not in locations['districts']:
                            locations['districts'].append(dist_val)
        
        logger.info(f"Extracted locations: {locations}")
        
        # Intent-based routing (Rasa or pattern matching)
        final_intent = None
        
        if rasa_intent and rasa_confidence > 0.6:
            final_intent = rasa_intent
            logger.info(f"Using Rasa intent: {final_intent}")
        else:
            # Fallback to pattern matching
            patterns = {
                'greet': ['hello', 'hi', 'hey', 'namaste', 'ನಮಸ್ಕಾರ', 'नमस्ते'],
                'ask_state_list': ['show states', 'list states', 'all states', 'ರಾಜ್ಯಗಳು'],
                'compare_data': ['compare', 'vs', 'versus', 'difference'],
                'ask_rainfall_data': ['rainfall', 'rain', 'ಮಳೆ', 'वर्षा'],
                'ask_extraction_stage': ['extraction', 'stage', 'निष्कर्षण'],
                'ask_groundwater_info': ['water', 'groundwater', 'ನೀರು', 'data', 'info']
            }
            
            for intent, keywords in patterns.items():
                if any(kw in search_text for kw in keywords):
                    final_intent = intent
                    logger.info(f"Pattern matched intent: {final_intent}")
                    break
        
        # Handle intents (KEEP YOUR EXISTING INTENT HANDLING CODE)
        if final_intent == 'greet':
            bot_response = "Hello! I'm your INGRES AI assistant. I can provide groundwater data for any state or district in India. Try: 'Bangalore' or 'Karnataka rainfall'"
            suggestions = ['Karnataka', 'Maharashtra', 'Bangalore', 'Mysore', 'Show all states']
        
        elif final_intent == 'ask_state_list':
            bot_response = f"I have groundwater data for {len(states)} states across India."
            suggestions = sorted(states[:20])
        
        elif final_intent == 'compare_data':
            entities_to_compare = locations['states'] + locations['districts']
            
            if len(entities_to_compare) >= 2:
                comparison_data = []
                
                for entity in entities_to_compare[:3]:
                    if entity in states:
                        stats = crud.get_statistics(db, entity)
                        if stats:
                            comparison_data.append({
                                'name': entity,
                                'type': 'State',
                                'rainfall': stats['avg_rainfall'],
                                'extraction': stats['avg_extraction_stage']
                            })
                    else:
                        data = crud.get_data_by_district(db, entity)
                        if data:
                            d = data[0]
                            comparison_data.append({
                                'name': d.district,
                                'type': 'District',
                                'rainfall': d.rainfall_mm or 0,
                                'extraction': d.stage_of_gw_extraction or 0,
                                'state': d.state
                            })
                
                if comparison_data:
                    bot_response = "Here's the comparison of groundwater data:"
                    chart_data = {'type': 'comparison', 'data': comparison_data}
                else:
                    bot_response = "I found the locations but couldn't retrieve data."
            else:
                bot_response = "Please specify at least two locations to compare."
        
        elif final_intent == 'ask_rainfall_data':
            matched_location = None
            location_type = None
            
            if locations['districts']:
                matched_location = locations['districts'][0]
                location_type = 'district'
            elif locations['states']:
                matched_location = locations['states'][0]
                location_type = 'state'
            
            if matched_location:
                if location_type == 'state':
                    data_results = crud.get_data_by_state(db, matched_location)
                    stats = crud.get_statistics(db, matched_location)
                    if stats:
                        bot_response = f"Rainfall data for {matched_location}: Average rainfall is {stats['avg_rainfall']:.2f}mm across {stats['total_records']} districts."
                        chart_data = {
                            'type': 'rainfall',
                            'data': [{'district': d.district, 'rainfall': d.rainfall_mm} for d in data_results[:10] if d.rainfall_mm]
                        }
                else:
                    data_results = crud.get_data_by_district(db, matched_location)
                    if data_results:
                        d = data_results[0]
                        bot_response = f"Rainfall in {d.district}: {d.rainfall_mm:.2f}mm"
            else:
                bot_response = "Please specify a location for rainfall data."
        
        elif final_intent == 'ask_extraction_stage':
            matched_location = None
            location_type = None
            
            if locations['districts']:
                matched_location = locations['districts'][0]
                location_type = 'district'
            elif locations['states']:
                matched_location = locations['states'][0]
                location_type = 'state'
            
            if matched_location:
                if location_type == 'state':
                    data_results = crud.get_data_by_state(db, matched_location)
                    stats = crud.get_statistics(db, matched_location)
                    if stats:
                        bot_response = f"Groundwater extraction in {matched_location}: Average extraction stage is {stats['avg_extraction_stage']:.2f}%"
                        chart_data = {
                            'type': 'extraction',
                            'data': [{'district': d.district, 'extraction': d.stage_of_gw_extraction} for d in data_results[:10] if d.stage_of_gw_extraction]
                        }
                else:
                    data_results = crud.get_data_by_district(db, matched_location)
                    if data_results:
                        d = data_results[0]
                        bot_response = f"Extraction stage in {d.district}: {d.stage_of_gw_extraction:.2f}%"
            else:
                bot_response = "Please specify a location."
        
        else:  # ask_groundwater_info or default
            if locations['districts']:
                matched_district = locations['districts'][0]
                data_results = crud.get_data_by_district(db, matched_district)
                
                if data_results:
                    d = data_results[0]
                    bot_response = f"Groundwater data for {matched_district} in {d.state}:"
                    details = []
                    if d.rainfall_mm:
                        details.append(f"Rainfall: {d.rainfall_mm:.2f}mm")
                    if d.stage_of_gw_extraction:
                        details.append(f"Extraction: {d.stage_of_gw_extraction:.2f}%")
                    if d.ground_water_recharge:
                        details.append(f"GW Recharge: {d.ground_water_recharge:.2f} ham")
                    if d.net_gw_availability:
                        details.append(f"Net Availability: {d.net_gw_availability:.2f} ham")
                    
                    if details:
                        bot_response += " " + ", ".join(details)
                    
                    districts_in_state = crud.get_districts_by_state(db, d.state)
                    suggestions = [dist for dist in districts_in_state if dist != matched_district][:8]
            
            elif locations['states']:
                matched_state = locations['states'][0]
                data_results = crud.get_data_by_state(db, matched_state)
                stats = crud.get_statistics(db, matched_state)
                
                if stats:
                    bot_response = f"Groundwater data for {matched_state}: Average rainfall: {stats['avg_rainfall']:.2f}mm, Average extraction: {stats['avg_extraction_stage']:.2f}%, Total districts: {stats['total_records']}"
                    
                    chart_data = {
                        'type': 'state_overview',
                        'data': [
                            {'name': 'Rainfall (mm)', 'value': stats['avg_rainfall']},
                            {'name': 'Extraction (%)', 'value': stats['avg_extraction_stage']}
                        ]
                    }
                    
                    districts = crud.get_districts_by_state(db, matched_state)
                    suggestions = districts[:12]
            
            else:
                bot_response = "I couldn't find that location. Try: 'Bangalore', 'Mysore', or 'Karnataka'"
                suggestions = ['Karnataka', 'Maharashtra', 'Bangalore', 'Mysore', 'Mumbai']
        
        logger.info(f"Response: {bot_response[:100]}...")
        
        # Translate back
        if user_language != 'en' and bot_response:
            try:
                bot_response = translator.translate_text(bot_response, user_language, 'en')
            except:
                pass
        
        # Format data
        formatted_data = []
        for d in data_results[:15]:
            formatted_data.append({
                "state": d.state,
                "district": d.district,
                "rainfall": round(d.rainfall_mm, 2) if d.rainfall_mm else None,
                "extraction_stage": round(d.stage_of_gw_extraction, 2) if d.stage_of_gw_extraction else None,
                "gw_recharge": round(d.ground_water_recharge, 2) if d.ground_water_recharge else None,
                "net_availability": round(d.net_gw_availability, 2) if d.net_gw_availability else None
            })
        
        return schemas.ChatResponse(
            response=bot_response,
            data=formatted_data if formatted_data else None,
            suggestions=suggestions if suggestions else None,
            chart_data=chart_data
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/states", response_model=List[str])
def get_states(db: Session = Depends(get_db)):
    return crud.get_all_states(db)

@app.get("/districts/{state}", response_model=List[str])
def get_districts(state: str, db: Session = Depends(get_db)):
    return crud.get_districts_by_state(db, state)

@app.get("/data/{state}")
def get_state_data(state: str, db: Session = Depends(get_db)):
    data = crud.get_data_by_state(db, state)
    return [schemas.GroundwaterDataSchema.from_orm(d) for d in data]

@app.get("/stats/{state}")
def get_state_stats(state: str, db: Session = Depends(get_db)):
    stats = crud.get_statistics(db, state)
    if not stats:
        raise HTTPException(status_code=404, detail="State not found")
    return stats

@app.get("/stats/total")
def get_total_stats(db: Session = Depends(get_db)):
    total_records = db.query(models.GroundwaterData).count()
    total_states = db.query(models.GroundwaterData.state).distinct().count()
    total_districts = db.query(models.GroundwaterData.district).distinct().count()
    return {
        "total_records": total_records,
        "total_states": total_states,
        "total_districts": total_districts,
        "rasa_enabled": USE_RASA
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "rasa_enabled": USE_RASA,
        "translation": "deep-translator"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
