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
                  参与者及其用户故事：
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

    def generate(self, system_desc: str, actors: list[dict]) -> List[dict]:
        """生成完整的基本流程步骤"""
        result = self.chain0.invoke({"system_desc": system_desc, "actors": actors,
                                     "format_instructions": self.parser.get_format_instructions()})
        return result

    # def regenerate_one_step(self, system_desc: str, actor: Dict, user_story: Dict, old_step: str,
    #                         suggestion: str) -> str:
    #     """重新生成步骤"""
    #     result = self.chain1.invoke(
    #         {"system_desc": system_desc, "actor": actor, "user_story": user_story, "old_step": old_step,
    #          "suggestion": suggestion,
    #          "format_instructions": self.parser.get_format_instructions()})
    #     return result
    #
    # def regenerate(self, system_desc: str, actor: Dict, user_story: Dict, old_steps: List[str], suggestion: str) -> \
    # List[str]:
    #     """重新生成步骤"""
    #     result = self.chain2.invoke(
    #         {"system_desc": system_desc, "actor": actor, "user_story": user_story, "old_steps": old_steps,
    #          "suggestion": suggestion,
    #          "format_instructions": self.parser.get_format_instructions()})
    #     return result
    def regenerate(self, system_desc: str, actors: list[dict], suggestion: str):
        pass
