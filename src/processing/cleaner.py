import re
from bs4 import BeautifulSoup
from logs.logger import logger

# ====== CLEANING FUNCTION ======
def clean_text(text: str, message_id: str = None) -> str:
    if not text:
        return ""
    
    try:
        # Remove HTML
        soup = BeautifulSoup(text, "html.parser")
        cleaned = soup.get_text(separator=" ")
        
        # Remove space, table
        cleaned = re.sub(r"\s+", " ", cleaned)
        
        # Remove invisible and non-printable characters
        cleaned = re.sub(r"[^\x20-\x7EÀ-ÿ]", "", cleaned)
        
        return cleaned.strip()
    except Exception as e:
        logger.error(
            "Cleaner failed",
            message_id=message_id,
            error=str(e)
        )
        raise