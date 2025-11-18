from googletrans import Translator
from typing import Optional

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'hi': 'hindi',
            'en': 'english',
            'ta': 'tamil',
            'te': 'telugu',
            'kn': 'kannada',
            'ml': 'malayalam',
            'bn': 'bengali',
            'mr': 'marathi',
            'gu': 'gujarati'
        }
    
    def translate_text(self, text: str, target_lang: str = 'en', source_lang: str = 'auto') -> Optional[str]:
        """Translate text to target language"""
        try:
            if target_lang not in self.supported_languages:
                target_lang = 'en'
            
            translation = self.translator.translate(text, dest=target_lang, src=source_lang)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except:
            return 'en'