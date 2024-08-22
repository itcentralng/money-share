from typing import Optional
from pydantic import BaseModel


class UserType(BaseModel):
    full_name: Optional[str] = None
    phone_number: str
    pin: str
