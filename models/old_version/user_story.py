from pydantic import BaseModel
from typing import List

class UserStory(BaseModel):
    id: str
    description: str
    pre_conditions: List[str]
    post_conditions: List[str]
    basic_flow: List[dict]  # [{step:1, actor:"User", action:"..."}]
    extended_flow: List[dict]