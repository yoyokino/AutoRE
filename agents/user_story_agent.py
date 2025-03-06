from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class UserStoryAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template("""
                  根据系统描述、参与者列表、当事者参与者及其描述，生成当事者参与者的用户故事列表：
                  系统描述：
                  {system_desc}
                  参与者列表：
                  {actors}
                  当事者参与者：
                  {actor}

                  要求：
                  1. 每个用户故事必须仅包含user_story字段，该字段为一句话描述的用户故事形式的需求
                  2. 用户故事数量建议3-5个，必须是当事者参与者的用户故事
                  3. 返回示例格式：
                     [{{"user_story": "作为一个 收银员， 我想要 处理商品结算， 以便于 顾客可以支付完成购物且系统可以记录账目"}},...]

                  返回JSON格式：{format_instructions}
                """)  # 修正处：使用双大括号转义示例中的JSON符号
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template("""
                  根据系统描述、参与者列表、当事者参与者及其描述、一条原本的用户故事、客户的修改意见，生成当这条用户故事的修改版：
                  系统描述：
                  {system_desc}
                  参与者列表：
                  {actors}
                  当事者参与者：
                  {actor}
                  原本的用户故事：
                  {old_user_story}
                  客户的修改意见：
                  {suggestion}

                  要求：
                  1. 返回示例格式：
                     {{"user_story": "作为一个 收银员， 我想要 处理商品结算， 以便于 顾客可以支付完成购物且系统可以记录账目"}}
                  2. 重新生成的用户故事必须仅包含user_story字段，该字段为一句话描述的用户故事形式的需求

                  返回JSON格式：{format_instructions}
                """)  # 修正处：使用双大括号转义示例中的JSON符号
        self.chain1 = self.prompt1 | llm | self.parser

    def generate(self, system_desc: str, actors: list[dict], actor: dict) -> List[Dict]:
        """生成初始参与者"""
        result = self.chain0.invoke({
            "system_desc": system_desc,
            "actors": actors,
            "actor": actor,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result

    def regenerate(self, system_desc: str, actors: list[dict], actor: dict, old_user_story: dict,
                   suggestion: str) -> Dict:
        """生成初始参与者"""
        result = self.chain1.invoke({
            "system_desc": system_desc,
            "actors": actors,
            "actor": actor,
            "old_user_story": old_user_story,
            "suggestion": suggestion,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result
