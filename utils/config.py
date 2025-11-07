# src/config.py  
from pydantic_settings import BaseSettings, SettingsConfigDict

# ====== CONFIGURATION ======
class Settings(BaseSettings):
    # minIO
    minio_tracking: str
    minio_id: str
    minio_mdp: str
    prefix_bucket: str
    bucket1: str
    bucket2: str
    bucket3: str
    
    # RabbitMQ
    rabbitmq_host: str
    rabbitmq_port: str
    
    # Workers
    worker_name: str
    finance_queue: str
    embedding_queue: str
    
    # Milvus 
    milvus_yaml: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()