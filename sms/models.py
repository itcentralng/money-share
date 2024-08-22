from typing import Optional
from pydantic import BaseModel, Field


class SMSModel(BaseModel):
    date: Optional[str] = None
    from_: str = Field(alias=("from"))
    id: Optional[str] = None
    linkId: Optional[str] = None
    text: str
    to: str
    networkCode: Optional[str] = None
