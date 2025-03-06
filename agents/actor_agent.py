from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ActorAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt = ChatPromptTemplate.from_template("""
                  根据系统描述生成参与者列表：
                  {system_desc}

                  要求：
                  1. 每个参与者必须包含actor和description字段
                  2. 参与者数量建议3-5个
                  3. 返回示例格式：
                     [{{"actor": "用户", "description": "系统的主要使用者"}},...]

                  返回JSON格式：{format_instructions}
                """)  # 修正处：使用双大括号转义示例中的JSON符号
        self.chain = self.prompt | llm | self.parser

    def generate(self, system_desc: str) -> List[Dict]:
        """生成初始参与者"""
        result = self.chain.invoke({
            "system_desc": system_desc,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result
