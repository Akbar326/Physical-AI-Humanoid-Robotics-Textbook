import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cohere Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Qdrant Configuration
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Book Site Configuration
BOOK_SITE_URL = os.getenv("BOOK_SITE_URL", "https://physical-ai-humanoid-robotics-textb-topaz-theta.vercel.app/")

# Sitemap URL for discovering all book pages
SITEMAP_URL = f"{BOOK_SITE_URL.rstrip('/')}/sitemap.xml"

# Collection name for Qdrant
COLLECTION_NAME = "rag_embedding"

# Configuration validation
def validate_config():
    """Validate that required configuration values are present."""
    missing_vars = []

    if not COHERE_API_KEY:
        missing_vars.append("COHERE_API_KEY")

    if not OPENAI_API_KEY:
        missing_vars.append("OPENAI_API_KEY")

    if not QDRANT_API_KEY:
        missing_vars.append("QDRANT_API_KEY")

    if not QDRANT_HOST:
        missing_vars.append("QDRANT_HOST")

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return True