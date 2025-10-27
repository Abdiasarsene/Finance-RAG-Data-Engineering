from langdetect import detect, DetectorFactory
from logs.logger import logger

DetectorFactory.seed = 0  # for stable results

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