from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class BasicFlowAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template("""
                  根据系统描述、参与者、用户故事，生成完整的基本流程步骤：
                  系统描述：
                  {system_desc}
                  参与者：
                  {actor}
                  用户故事：
                  {user_story}

                  要求：
                  1. 每个步骤内容必须只包含一个字符串
                  2. actor必须是"User"或"System"之一
                  3. action必须是清晰的动作描述
                  4. 返回示例格式：
                     [
                        "(User) 客户 应 带着商品到达POS收银台购买",
                        "(User) 收银员 应 开始新的销售。",
                        "(System) CoCoME 应 将开始新的销售。",
                        "(User) 收银员 应 输入项目标识。",
                        "(System) 当 开始新的销售时 ， CoCoME 应 记录每个销售项目，并提供项目描述和运行总额。(循环 4 ~ 5 直到输入结束)",
                        "(System) 当 销售结束时 ， CoCoME 应 提交合计计算的税款。",
                        "(User) 收银员 应 告诉顾客总额并要求付款。",
                        "(User) 客户 应 支付费用。(选择 a8，b8，c8，d8)",
                        "(System) 当 付款结束后 ， CoCoME 应 处理。",
                        "(System) 当 完成销售时 ， CoCoME 应 记录完成销售，并将信息发送到外部会计和库存系统，并提交收据。"
                     ]
                     
                  返回JSON格式：{format_instructions}
                """)
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template("""
                  根据现有步骤和修改建议，重新生成步骤：
                  系统描述：
                  {system_desc}
                  参与者：
                  {actor}
                  现有用户故事：
                  {user_story}
                  原有单步基本流程：
                  {old_step}
                  修改建议：
                  {suggestion}

                  要求：
                  1. 返回的单个步骤内容必须只包含一个new_step字段
                  2. actor必须是原本单步基本流程中的"User"或"System"，不能改变
                  3. action必须是符合修改建议要求的、清晰的动作描述
                  4. 返回示例格式：{{"new_step": "(User) 客户 应 带着商品到达POS收银台购买"}}

                  返回JSON格式：{format_instructions}
                """)
        self.chain1 = self.prompt1 | llm | self.parser

        self.prompt2 = ChatPromptTemplate.from_template("""
                          根据现有步骤和修改建议，重新生成步骤：
                          系统描述：
                          {system_desc}
                          参与者：
                          {actor}
                          现有用户故事：
                          {user_story}
                          原有所有基本流程：
                          {old_steps}
                          修改建议：
                          {suggestion}

                          要求：
                          1. 返回的单个步骤内容必须只包含一个字符串列表
                          2. 每个字符串中，actor必须是"User"或"System"之一
                          3. 每个字符串中，action必须是符合修改建议要求的、清晰的动作描述
                          4. 返回示例格式：
                          [
                            "(User) 客户 应 带着商品和服务到达POS收银台购买",
                            "(User) 收银员 应 开始新的销售。",
                            "(System) CoCoME 应 将开始新的销售。",
                            "(User) 收银员 应 输入项目标识。",
                            "(System) 当 开始新的销售时 ， CoCoME 应 记录每个销售项目，并提供项目描述和运行总额。(循环 4 ~ 5 直到输入结束)",
                            "(System) 当 销售结束时 ， CoCoME 应 提交合计计算的税款。",
                            "(User) 收银员 应 告诉顾客总额并要求付款。",
                            "(User) 客户 应 支付费用。(选择 a8，b8，c8，d8)",
                            "(System) 当 付款结束后 ， CoCoME 应 处理。",
                            "(System) 当 完成销售时 ， CoCoME 应 记录完成销售，并将信息发送到外部会计和库存系统，并提交收据。"
                         ]

                          返回JSON格式：{format_instructions}
                        """)
        self.chain2 = self.prompt2 | llm | self.parser

    def generate(self, system_desc: str, actor: Dict, user_story: Dict) -> List[str]:
        """生成完整的基本流程步骤"""
        result = self.chain0.invoke({"system_desc": system_desc, "actor": actor, "user_story": user_story,
            "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate_one_step(self, system_desc: str, actor: Dict, user_story: Dict, old_step: str, suggestion: str) -> str:
        """重新生成步骤"""
        result = self.chain1.invoke(
            {"system_desc": system_desc, "actor": actor, "user_story": user_story, "old_step": old_step, "suggestion": suggestion,
                "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate(self, system_desc: str, actor: Dict, user_story: Dict, old_steps: List[str], suggestion: str) -> List[str]:
        """重新生成步骤"""
        result = self.chain2.invoke(
            {"system_desc": system_desc, "actor": actor, "user_story": user_story, "old_steps": old_steps, "suggestion": suggestion,
                "format_instructions": self.parser.get_format_instructions()})
        return result
