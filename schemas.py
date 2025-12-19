from pydantic import BaseModel
from typing import Optional

class URLCreate(BaseModel):
    url: str
    custom_alias: Optional[str] = None
    expires_in_seconds: Optional[int] = None
