from pydantic import BaseModel
from typing import List

class SystemEntity(BaseModel):
    name: str
    type: str  # Actor/Operation/DataStore等
    attributes: dict
    relations: List[str]