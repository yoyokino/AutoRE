from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ConditionAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()

        # 生成前后置条件的prompt
        self.prompt0 = ChatPromptTemplate.from_template("""
                  根据系统描述、系统实体信息、当事者参与者及其描述、用户故事，生成该用户故事的前后置条件：
                  系统描述：
                  {system_desc}
                  系统实体信息：
                  {entities}
                  当事者参与者：
                  {actor}
                  用户故事：
                  {user_story}

                  要求：
                  1. 必须包含pre_condition和post_condition两个字段
                  2. 条件必须是若干简短清晰的陈述句，pre_condition和post_condition两个字段只能有一个字符串，字符串里可以有多个语句，但不能是列表
                  3. 返回示例格式：
                     {{"pre_condition": "用户已登录系统", "post_condition": "结算信息已保存到数据库。库存信息已更新到数据库。"}}

                  返回JSON格式：{format_instructions}
                """)
        self.chain0 = self.prompt0 | llm | self.parser

        # 重新生成单个条件的prompt 
        self.prompt1 = ChatPromptTemplate.from_template("""
                  根据系统描述、系统实体信息、参与者列表、当事者参与者及其描述、用户故事、原有条件、修改建议，重新生成条件：
                  系统描述：
                  {system_desc}
                  系统实体信息：
                  {entities}
                  用户故事：
                  {user_story}
                  原有条件：
                  {old_condition}
                  修改建议：
                  {suggestion}

                  要求：
                  1. 根据两种条件类型(pre_condition和post_condition)重新生成两个对应字段
                  2. 条件必须是若干简短清晰的陈述句，pre_condition和post_condition两个字段只能有一个字符串，字符串里可以有多个语句，但不能是列表
                  3. 返回示例格式：
                     {{"pre_condition": "用户已登录系统。", "post_condition": "结算信息已保存到数据库。库存信息已更新到数据库。"}}

                  返回JSON格式：{format_instructions}
                """)
        self.chain1 = self.prompt1 | llm | self.parser

    def generate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict) -> Dict:
        """生成用户故事的前后置条件"""
        result = self.chain0.invoke({
            "system_desc": system_desc,
            "entities": entities,
            "actor": actor,
            "user_story": user_story,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result

    def regenerate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict,
                   old_condition: dict, suggestion: str) -> dict:
        """重新生成单个条件"""
        result = self.chain1.invoke({
            "system_desc": system_desc,
            "entities": entities,
            "actor": actor,
            "user_story": user_story,
            "old_condition": old_condition,
            "suggestion": suggestion,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result
