from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class EntityAnalysisAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template("""
                  根据软件系统描述、参与者及其用户故事，分析软件系统中确定存在的实体，生成完整的实体及其属性的列表：
                  系统描述：
                  {system_desc}
                  所有参与者及其用户故事：
                  {actors}

                  要求：
                  1. 每个实体内容包含一个entity字段和一个attributes字段
                  2. entity字段为实体的名称
                  3. attributes字段为实体属性的列表，列表的每一项包括type和content字段，分别代表属性的类型（int/float/string/bool/date/blob）和名称
                  4. 返回示例格式：
                     [
                        {{
                            "entity": "商品",
                            "attributes": [
                                {{
                                    "type": "string"
                                    "content": "名称"
                                }},
                                {{
                                    "type": "int"
                                    "content": "库存数量"
                                }},
                                {{
                                    "type": "blob"
                                    "content": "商品图片"
                                }},
                                ......
                            ]
                        }},
                        ......
                     ]

                  返回JSON格式：{format_instructions}
                  """)
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
            3. The "attributes" field is a list of attributes, where each item includes "type" and "content" fields, representing the attribute's type (int/float/string/bool/date/blob) and name, respectively.
            4. Example format:
            {
                "entity": "Product",
                "attributes": [
                    {
                        "type": "string",
                        "content": "Name"
                    },
                    {
                        "type": "int",
                        "content": "Inventory Quantity"
                    },
                    {
                        "type": "blob",
                        "content": "Product Image"
                    }
                    ...
                ]
            }
            
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
            3. The "attributes" field is a list of attributes, each containing "type" and "content" fields, indicating the attribute type (int/float/string/bool/date/blob) and its name respectively.
            4. Example format:
            {
                "entity": "Product",
                "attributes": [
                    {
                        "type": "string",
                        "content": "Name"
                    },
                    {
                        "type": "int",
                        "content": "Inventory Quantity"
                    },
                    {
                        "type": "blob",
                        "content": "Product Image"
                    }
                    ...
                ]
            }
            
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
