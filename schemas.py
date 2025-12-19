from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    url: str
    custom_alias: Optional[str] = None
    expires_in_seconds: Optional[int] = None

class URLStats(BaseModel):
    redirects: int
    created_at: datetime
    last_accessed: Optional[datetime] = None
