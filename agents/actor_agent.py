from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ActorAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt = ChatPromptTemplate.from_template(
            """Generate a list of actors based on the system description:
            {system_desc}
            
            Requirements:
            1. Each actor must include "actor" and "description" fields.
            2. Example of the expected returned format:
               [{{"actor": "User", "description": "The primary user of the system"}}, ...]
            
            Return in JSON format: {format_instructions}"""
        )  # 修正处：使用双大括号转义示例中的JSON符号
        self.chain = self.prompt | llm | self.parser

    def generate(self, system_desc: str) -> List[Dict]:
        """生成初始参与者"""
        result = self.chain.invoke({
            "system_desc": system_desc,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result
