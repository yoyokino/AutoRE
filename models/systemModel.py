from pydantic import BaseModel
from typing import List


class ExtendedFlowItem(BaseModel):
    type: str  # "Optional"/"Selection"/"Exception Handling"
    id: str
    title: str
    content: List[str] = []

    # example = {
    #     "type": "",
    #     "id": "",
    #     "title": "",
    #     "content": [
    #         "",
    #         "",
    #         ""
    #     ]
    # }


class UserStory(BaseModel):
    user_story: str
    pre_condition: str = None
    post_condition: str = None
    basic_flow: List[str] = []
    extended_flow: List[ExtendedFlowItem] = []


class Actor(BaseModel):
    actor: str
    description: str
    user_stories: List[UserStory] = []


class EntityAttribute(BaseModel):
    type: str
    content: str


class Entity(BaseModel):
    entity: str
    attributes: List[EntityAttribute] = []


class SystemModel(BaseModel):
    system_description: str = ""
    actors: List[Actor] = []
    entities: List[Entity] = []

