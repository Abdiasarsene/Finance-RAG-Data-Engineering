# src/processing/language_detector.py
from langdetect import detect, DetectorFactory
from logs.logger import logger

# ====== DETECT LANGUAGE ======
DetectorFactory.seed = 0

def detect_language(text: str, message_id: str = None) -> str:
    if not text:
        return "unknown"
    
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        logger.error(
            "Language detection failed",
            message_id=message_id,
            error=str(e)
        )
        return "unknown"