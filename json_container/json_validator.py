import json
from pathlib import Path
from jsonschema import validate, ValidationError
from logs.logger import logger
from json_container.schema_loader import load_base_schema  # mieux que de recharger le fichier ici

def validate_json(json_data: dict, message_id: str = None) -> bool:
    try:
        validate(instance=json_data, schema=load_base_schema())
        return True
    except ValidationError as e:
        logger.error(
            "JSON validation failed",
            message_id=message_id,
            error=e.message
        )
        return False
    except Exception as e:
        logger.error(
            "JSON validation unexpected error",
            message_id=message_id,
            error=str(e)
        )
        raise