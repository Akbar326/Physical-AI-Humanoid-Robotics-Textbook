from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime


class Document(BaseModel):
    """
    Represents a document chunk from the documentation site that has been processed and embedded for semantic search.
    """
    id: str = str(uuid.uuid4())
    content: str
    source_url: str
    title: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = {}
    created_at: datetime = datetime.now()