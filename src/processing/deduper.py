from logs.logger import logger

def dedupe_document(text: str, message_id: str = None) -> str:
    if not text:
        return ""
    
    try:
        paragraphs = text.split(". ")
        seen = set()
        deduped_paragraphs = []
        
        for p in paragraphs:
            key = hash(p.strip().lower())
            if key not in seen:
                seen.add(key)
                deduped_paragraphs.append(p.strip())
        
        return ". ".join(deduped_paragraphs)
    except Exception as e:
        logger.error(
            "Deduper failed",
            message_id=message_id,
            error=str(e)
        )
        raise