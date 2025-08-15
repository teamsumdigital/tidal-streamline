"""
Configuration management for Tidal Streamline API
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server Configuration
    PORT: int = Field(default=8008, description="Server port")
    DEBUG_MODE: bool = Field(default=True, description="Debug mode")
    
    # Database Configuration (Supabase)
    SUPABASE_URL: str = Field(..., description="Supabase project URL")
    SUPABASE_SERVICE_KEY: str = Field(..., description="Supabase service role key")
    
    # AI Services
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4", description="OpenAI model to use")
    
    # Vector Store (Pinecone)
    PINECONE_API_KEY: str = Field(default="pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe", description="Pinecone API key")
    PINECONE_INDEX_NAME: str = Field(default="tidal-streamline", description="Pinecone index name")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")
    EMBEDDING_DIMENSION: int = Field(default=1536, description="Embedding vector dimension")
    
    # Application Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Tidal Streamline"
    
    # Regional Configuration
    DEFAULT_REGIONS: list = Field(
        default=[
            "United States",
            "Philippines", 
            "Latin America",
            "South Africa"
        ],
        description="Default regions for salary analysis"
    )
    
    # Salary Calculation
    US_SALARY_BASELINE: bool = Field(default=True, description="Use US salaries as baseline")
    DEFAULT_SAVINGS_RATES: dict = Field(
        default={
            "Philippines": 0.71,  # 71% savings vs US
            "Latin America": 0.58,  # 58% savings vs US  
            "South Africa": 0.48,   # 48% savings vs US
        },
        description="Default savings rates by region"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()