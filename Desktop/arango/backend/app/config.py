"""
Configuration management for the Drug Interaction Checker API
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # ArangoDB Configuration
    ARANGO_HOST: str = os.getenv("ARANGO_HOST", "https://d8c1701e2a10.arangodb.cloud:8529")
    ARANGO_DB: str = os.getenv("ARANGO_DB", "drug_interation_db")
    ARANGO_USER: str = os.getenv("ARANGO_USER", "root")
    ARANGO_PASSWORD: str = os.getenv("ARANGO_PASSWORD", "")
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    # CORS origins - can be set via environment variable or defaults
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    ).split(",") if os.getenv("CORS_ORIGINS") else ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"]
    
    # Validation
    MIN_DRUGS_FOR_CHECK: int = 2
    MAX_DRUGS_FOR_CHECK: int = 20
    DRUG_SEARCH_LIMIT: int = 20
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required settings are present"""
        if not all([cls.ARANGO_HOST, cls.ARANGO_DB, cls.ARANGO_USER, cls.ARANGO_PASSWORD]):
            raise ValueError(
                "Missing required ArangoDB configuration. "
                "Please set ARANGO_HOST, ARANGO_DB, ARANGO_USER, and ARANGO_PASSWORD in .env file"
            )

# Create settings instance
settings = Settings()

