from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn

from .models import ChatQuery, ChatResponse, TranslationRequest
from .database import get_db, create_mock_data, GroundwaterData
from .nlp_engine import SimpleNLPEngine
from .visualization import VisualizationEngine
from .translation import TranslationService

app = FastAPI(title="Groundwater Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
nlp_engine = SimpleNLPEngine()
viz_engine = VisualizationEngine()
translation_service = TranslationService()

@app.on_event("startup")
async def startup_event():
    """Initialize mock data on startup"""
    create_mock_data()

@app.post("/query", response_model=ChatResponse)
async def process_chat_query(query: ChatQuery, db: Session = Depends(get_db)):
    """Main endpoint for processing chat queries"""
    try:
        # Detect language and translate to English if needed
        if query.language != 'en':
            detected_lang = translation_service.detect_language(query.message)
            english_text = translation_service.translate_text(query.message, 'en', detected_lang)
        else:
            english_text = query.message
            detected_lang = 'en'
        
        # Process query with NLP
        nlp_result = nlp_engine.process_query(english_text)
        
        # Fetch data from database based on entities
        data = fetch_groundwater_data(db, nlp_result['entities'])
        
        # Generate visualization
        chart_data = viz_engine.generate_chart(data, nlp_result['intent'], nlp_result['entities'])
        
        # Generate response text
        response_text = generate_response_text(nlp_result, data, nlp_result['entities'])
        
        # Translate response back to user's language if needed
        if query.language != 'en':
            response_text = translation_service.translate_text(response_text, query.language, 'en')
        
        return ChatResponse(
            text=response_text,
            chart_data=chart_data,
            chart_type=nlp_result['intent'],
            raw_data=data,
            intent=nlp_result['intent'],
            entities=nlp_result['entities']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """Standalone translation endpoint"""
    translated_text = translation_service.translate_text(
        request.text, request.target_lang, request.source_lang
    )
    return {"translated_text": translated_text}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "groundwater-chatbot"}

def fetch_groundwater_data(db: Session, entities: Dict[str, Any]) -> List[Dict]:
    """Fetch groundwater data based on extracted entities"""
    query = db.query(GroundwaterData)
    
    if entities.get('state'):
        query = query.filter(GroundwaterData.state == entities['state'])
    
    if entities.get('district'):
        query = query.filter(GroundwaterData.district == entities['district'])
    
    if entities.get('year'):
        query = query.filter(GroundwaterData.year == entities['year'])
    
    if entities.get('time_period'):
        current_year = entities.get('year', 2024)
        start_year = current_year - entities['time_period']
        query = query.filter(GroundwaterData.year >= start_year)
    
    results = query.limit(100).all()
    
    return [
        {
            "state": item.state,
            "district": item.district,
            "year": item.year,
            "month": item.month,
            "groundwater_level": item.groundwater_level,
            "rainfall": item.rainfall,
            "water_quality": item.water_quality,
            "category": item.category
        }
        for item in results
    ]

def generate_response_text(nlp_result: Dict, data: List[Dict], entities: Dict) -> str:
    """Generate natural language response based on data and intent"""
    intent = nlp_result['intent']
    
    if not data:
        return "I couldn't find any data matching your query. Please try different parameters."
    
    if intent == "groundwater_level":
        avg_level = sum(item['groundwater_level'] for item in data) / len(data)
        location = entities.get('district', entities.get('state', 'the region'))
        return f"The average groundwater level in {location} is {avg_level:.2f} meters. {get_water_level_insight(avg_level)}"
    
    elif intent == "trends":
        return f"Here are the groundwater trends for {entities.get('state', 'the selected region')} over the past {entities.get('time_period', 5)} years."
    
    elif intent == "comparison":
        return f"Comparison of groundwater levels across different locations in {entities.get('state', 'the selected region')}."
    
    elif intent == "water_quality":
        quality_counts = {}
        for item in data:
            quality = item['water_quality']
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        return f"Water quality distribution in {entities.get('state', 'the region')}: {', '.join([f'{count} locations {quality}' for quality, count in quality_counts.items()])}."
    
    return "Here's the groundwater data you requested."

def get_water_level_insight(level: float) -> str:
    """Provide insight based on groundwater level"""
    if level < 5:
        return "This indicates critical water levels that need attention."
    elif level < 10:
        return "The water levels are moderate but should be monitored."
    else:
        return "The water levels are in a safe range."

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)