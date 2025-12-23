from pydantic import BaseModel
from typing import Optional

class SetFaceRequest(BaseModel):
    group_id: int
    name: str
    image: str        # Base64
    count: int = 1
    sex: Optional[int] = 0
    age: Optional[int] = None
    nation: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
