from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class EntityAnalysisAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template(
            """Based on the system description, actors, and their user stories, analyze the entities that certainly exist in the software system and generate a complete list of entities along with their attributes:
            
            System Description:  
            {system_desc}
            
            All Actors and Their User Stories:  
            {actors}
            
            Requirements:  
            1. Each entity must include one "entity" field and one "attributes" field, and the number of entities should be between 2 and 3.
            2. The "entity" field specifies the name of the entity.  
            3. The "attributes" field is a list of attributes, each containing both "type" (int/float/string/bool/date/blob) and "content" (attribute name) fields. 
            4. The generated attributes must be the most important attributes of the entity, and the number should be between 2 and 3.
            4. Example format:
            [
                {{
                    "entity": "Product",
                    "attributes": [
                        {{
                            "type": "string",
                            "content": "Name"
                        }},
                        {{
                            "type": "int",
                            "content": "Inventory Quantity"
                        }},
                        {{
                            "type": "blob",
                            "content": "Product Image"
                        }}
                        ...
                    ]
                }},
                ...
            ]
            
            Return in JSON format: {format_instructions}""")
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template(
            """Based on the description of the software system, all actors and their User-Stories, an originally analyzed potential entity in the software system, and incorporating the user's modification suggestions, regenerate this entity and its attribute list:
            
            System Description:
            {system_desc}
            
            All Actors and their User-Stories:
            {actors}
            
            Originally Analyzed Potential Entity:
            {entity}
            
            User Suggestions:
            {suggestion}
            
            Requirements:
            1. The entity content must include an "entity" field and an "attributes" field.
            2. The "entity" field represents the entity's name.
            3. The newly generated attributes must be the most important attributes of the entity, and the quantity should not be too large (if there are no suggestions, it should be the number should be between 2 and 3).
            4. The "attributes" field is a list of attributes, where each item includes "type" and "content" fields, representing the attribute's type (int/float/string/bool/date/blob) and name, respectively.
            5. Example format:
            {{
                "entity": "Product",
                "attributes": [
                    {{
                        "type": "string",
                        "content": "Name"
                    }},
                    {{
                        "type": "int",
                        "content": "Inventory Quantity"
                    }},
                    {{
                        "type": "blob",
                        "content": "Product Image"
                    }}
                    ...
                ]
            }}
            
            Return in JSON format: {format_instructions}""")
        self.chain1 = self.prompt1 | llm | self.parser

        self.prompt2 = ChatPromptTemplate.from_template(
            """Based on the software system description, all actors and their User-Stories, other possible existing entities in the software system, and incorporating the user's suggestions, generate a new entity and its attribute list:
            
            System Description:
            {system_desc}
            
            All Actors and their User-Stories:
            {actors}
            
            Other Possible Entities in the Software System:
            {entities}
            
            User Suggestions:
            {suggestion}
            
            Requirements:
            1. The new entity must include an "entity" field and an "attributes" field.
            2. The "entity" field represents the name of the entity.
            3. The newly generated attributes must be the most important attributes of the entity, and the number should not be too large (if there are no suggestions, it should be between 2 and 3).
            4. The "attributes" field is a list of attributes, each containing "type" and "content" fields, indicating the attribute type (int/float/string/bool/date/blob) and its name respectively.
            5. Example format:
            {{
                "entity": "Product",
                "attributes": [
                    {{
                        "type": "string",
                        "content": "Name"
                    }},
                    {{
                        "type": "int",
                        "content": "Inventory Quantity"
                    }},
                    {{
                        "type": "blob",
                        "content": "Product Image"
                    }}
                    ...
                ]
            }}
            
            Return in JSON format: {format_instructions}""")
        self.chain2 = self.prompt2 | llm | self.parser

    def generate(self, system_desc: str, actors: list[dict]) -> List[dict]:
        result = self.chain0.invoke({"system_desc": system_desc, "actors": actors,
                                     "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate_one(self, system_desc: str, actors: list[dict], entity: dict, suggestion: str) -> dict:
        result = self.chain1.invoke(
            {"system_desc": system_desc, "actors": actors, "entity": entity, "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result

    def add_one(self, system_desc: str, actors: list[dict], entities: list[dict], suggestion: str) -> dict:
        result = self.chain2.invoke(
            {"system_desc": system_desc, "actors": actors, "entities": entities, "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result
