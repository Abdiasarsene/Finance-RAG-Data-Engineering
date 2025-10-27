# logs/logger.py  
import logging
import sys
import structlog

# ====== LOGGING PYTHON ======
logging.basicConfig(
    format="%(message)",
    stream=sys.stdout,
    level=logging.INFO
)

# ====== CONFIG STRUCTLOG ======
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True
)

# ====== LOGGER ======
logger = structlog.get_logger()