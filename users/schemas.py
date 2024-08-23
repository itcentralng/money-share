from typing import Optional
from pydantic import BaseModel


class UserType(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    phone_number: str
    pin: str
