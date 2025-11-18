import re
import spacy
from typing import Dict, Any, List
from datetime import datetime

class SimpleNLPEngine:
    def __init__(self):
        # Load small English model for basic NLP
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Spacy model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Define patterns for groundwater queries
        self.patterns = {
            'groundwater_level': [
                r'groundwater level',
                r'water level',
                r'water table',
                r'groundwater'
            ],
            'water_quality': [
                r'water quality',
                r'quality of water',
                r'contamination',
                r'pollution'
            ],
            'trends': [
                r'trend',
                r'over time',
                r'last \d+ years',
                r'historical'
            ],
            'comparison': [
                r'compare',
                r'comparison',
                r'difference between',
                r'versus'
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text using rule-based approach"""
        entities = {
            'state': None,
            'district': None,
            'year': datetime.now().year,
            'time_period': None,
            'comparison_entity': None
        }
        
        # State extraction
        states = [
            'karnataka', 'maharashtra', 'tamil nadu', 'uttar pradesh', 
            'rajasthan', 'gujarat', 'west bengal', 'bihar', 'andhra pradesh'
        ]
        
        # District extraction (sample)
        districts = [
            'bangalore', 'mumbai', 'pune', 'chennai', 'delhi', 'hyderabad',
            'kolkata', 'jaipur', 'lucknow', 'ahmedabad'
        ]
        
        text_lower = text.lower()
        
        # Extract state
        for state in states:
            if state in text_lower:
                entities['state'] = state.title()
                break
        
        # Extract district
        for district in districts:
            if district in text_lower:
                entities['district'] = district.title()
                break
        
        # Extract year
        year_match = re.search(r'\b(20\d{2})\b', text)
        if year_match:
            entities['year'] = int(year_match.group(1))
        
        # Extract time period
        if 'last 5 years' in text_lower:
            entities['time_period'] = 5
        elif 'last 3 years' in text_lower:
            entities['time_period'] = 3
        elif 'this year' in text_lower:
            entities['year'] = datetime.now().year
        
        return entities
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent based on patterns"""
        text_lower = text.lower()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return "groundwater_level"  # Default intent
    
    def process_query(self, text: str) -> Dict[str, Any]:
        """Process user query and extract intent and entities"""
        return {
            'intent': self.detect_intent(text),
            'entities': self.extract_entities(text),
            'original_text': text
        }