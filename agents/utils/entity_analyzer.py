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

        self.prompt1 = ChatPromptTemplate.from_template("""
                      根据软件系统描述、所有参与者及其用户故事、一个原本分析认为软件系统中可能存在的实体，结合用户的修改建议，重新生成这一个实体及其属性的列表：
                      系统描述：
                      {system_desc}
                      所有参与者及其用户故事：
                      {actors}
                      一个原本分析认为可能存在的实体：
                      {entity}
                      用户建议：
                      {suggestion}
                      

                      要求：
                      1. 该实体内容包含一个entity字段和一个attributes字段
                      2. entity字段为实体的名称
                      3. attributes字段为实体属性的列表，列表的每一项包括type和content字段，分别代表属性的类型（int/float/string/bool/date/blob）和名称
                      4. 返回示例格式：
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
                      }}

                      返回JSON格式：{format_instructions}
                      """)
        self.chain1 = self.prompt1 | llm | self.parser

        self.prompt2 = ChatPromptTemplate.from_template("""
                              根据软件系统描述、所有参与者及其用户故事、软件系统中其他可能存在的实体，结合用户的修改意见，生成一个新的实体及其属性的列表：
                              系统描述：
                              {system_desc}
                              所有参与者及其用户故事：
                              {actors}
                              软件系统中其他可能存在的实体：
                              {entities}
                              用户意见：
                              {suggestion}


                              要求：
                              1. 新的实体内容包含一个entity字段和一个attributes字段
                              2. entity字段为实体的名称
                              3. attributes字段为实体属性的列表，列表的每一项包括type和content字段，分别代表属性的类型（int/float/string/bool/date/blob）和名称
                              4. 返回示例格式：
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
                              }}

                              返回JSON格式：{format_instructions}
                              """)
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
