from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ExtendedFlowAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template("""
                    根据系统描述、参与者、用户故事，生成完整的拓展流程步骤：
                    系统描述：
                    {system_desc}
                    参与者：
                    {actor}
                    用户故事：
                    {user_story}
                    
                    拓展流程的示例如下：
                    (Optional) *a、 经理 在任意时刻，需要进行超控操作：
                     1、 (System) 系统 进入经理授权模式。
                     2、 (User) 经理或收银员 执行某一经理模式的操作。
                     3、 (System) 系统 回复到收银员授权模式。
                    (Exception Handling) *b、 系统 在任意时刻，失败：
                     1、 (User) 收银员 重启系统，登录，请求恢复上次状态。
                     2、 (System) 系统 重建上次状态。
                    (Optional) 2-3a、 顾客 告诉收银员其免税状况（例如，年长者本国人等）：
                     1、 (User) 收银员 进行核实，并输入免税状况编码。
                     2、 (System) 系统 记录读状况编码（在计算税金时使用）。
                    (Selection) 4a、 现金支付：
                     1、 (User) 收银员 输入收取的现金额。
                     2、 (System) 系统 显示找零金额，并弹出现金抽屉。
                     3、 (User) 收银员 放入收取的现金，并给顾客找零。
                     4、 (System) 系统 记录该现金支付。
                    (Selection) 4b、 信用卡支付：
                     1、 (User) 顾客 输入信用卡账户信息。
                     2、 (System) 系统 显示其支付信息以备验证。
                     3、 (User) 收银员 确认。
                    拓展流程格式解释：
                    以上为拓展流程格式模板。每一条拓展流程左起为(Optional)、(Exception Handling)或(Selection)，用以表示该条拓展流程的属性。
                    (Optional)：表示基本流程中可能出现的其他事件。
                    (Exception Handling) ：表示基本流程中可能发生的异常状况。
                    (Selection)：表示基本流程中选择的选项。
                    属性后接拓展流程顺序标号，编号的编写方法如下：
                    （*+小写字母）：表示在任意时刻发生的事件，字母只是序号并没有顺序的意义。
                    （数字+小写字母）：表示在基本流程N发生的事件，字母只是序号并没有顺序的意义。
                    （数字-数字+小写字母）：表示在基本流程M-N（第M条基本流程到第N条基本流程）发生的事件，字母只是序号并没有顺序的意义。
                    每一条拓展流程的句尾标点必须为冒号：
                    
                    要求：
                    1. 每个拓展流程包括type、id、title和content字段，content内容为一个字符串列表
                    2. type必须为Optional、Exception Handling或Selection之一
                    3. id需遵守以上编号编写方法
                    4. title为引发拓展流程的条件说明
                    5. content中，每一步的actor必须是"User"或"System"之一，每一步的action必须是清晰的动作描述
                    6. 返回示例格式：
                    [
                        {{
                            "type": "Optional",
                            "id": "*a",
                            "title": "经理 在任意时刻，需要进行超控操作",
                            "content": [
                                "(System) 系统 进入经理授权模式。",
                                "(User) 经理或收银员 执行某一经理模式的操作。",
                                "(System) 系统 回复到收银员授权模式。"
                            ]
                        }},
                        {{
                            "type": "Exception Handling",
                            "id": "*b",
                            "title": "系统 在任意时刻崩溃",
                            "content": [
                                "(User) 收银员 重启系统，登录，请求恢复上次状态。",
                                "(System) 系统 重建上次状态。"
                            ]
                        }},
                        {{
                            "type": "Selection",
                            "id": "4a",
                            "title": "现金支付",
                            "content": [
                                "(User) 收银员 输入收取的现金额。",
                                "(System) 系统 显示找零金额，并弹出现金抽屉。",
                                "(User) 收银员 放入收取的现金，并给顾客找零。",
                                "(System) 系统 记录该现金支付。"
                            ]
                        }},
                        ......
                    ]
                    
                    返回JSON格式：{format_instructions}
                    """)
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template("""
                  根据用户故事的内容和修改建议，重新生成一个拓展流程：
                  系统描述：
                  {system_desc}
                  参与者：
                  {actor}
                  现有用户故事：
                  {user_story}
                  原有拓展流程：
                  {old_flow}
                  修改建议：
                  {suggestion}
                    
                  拓展流程的示例如下：
                  (Optional) *a、 经理 在任意时刻，需要进行超控操作：
                   1、 (System) 系统 进入经理授权模式。
                   2、 (User) 经理或收银员 执行某一经理模式的操作。
                   3、 (System) 系统 回复到收银员授权模式。
                  (Exception Handling) *b、 系统 在任意时刻，失败：
                   1、 (User) 收银员 重启系统，登录，请求恢复上次状态。
                   2、 (System) 系统 重建上次状态。
                  (Optional) 2-3a、 顾客 告诉收银员其免税状况（例如，年长者本国人等）：
                   1、 (User) 收银员 进行核实，并输入免税状况编码。
                   2、 (System) 系统 记录读状况编码（在计算税金时使用）。
                  (Selection) 4a、 现金支付：
                   1、 (User) 收银员 输入收取的现金额。
                   2、 (System) 系统 显示找零金额，并弹出现金抽屉。
                   3、 (User) 收银员 放入收取的现金，并给顾客找零。
                   4、 (System) 系统 记录该现金支付。
                  (Selection) 4b、 信用卡支付：
                   1、 (User) 顾客 输入信用卡账户信息。
                   2、 (System) 系统 显示其支付信息以备验证。
                   3、 (User) 收银员 确认。
                  拓展流程格式解释：
                  以上为拓展流程格式模板。每一条拓展流程左起为(Optional)、(Exception Handling)或(Selection)，用以表示该条拓展流程的属性。
                  (Optional)：表示基本流程中可能出现的其他事件。
                  (Exception Handling) ：表示基本流程中可能发生的异常状况。
                  (Selection)：表示基本流程中选择的选项。
                  属性后接拓展流程顺序标号，编号的编写方法如下：
                  （*+小写字母）：表示在任意时刻发生的事件，字母只是序号并没有顺序的意义。
                  （数字+小写字母）：表示在基本流程N发生的事件，字母只是序号并没有顺序的意义。
                  （数字-数字+小写字母）：表示在基本流程M-N（第M条基本流程到第N条基本流程）发生的事件，字母只是序号并没有顺序的意义。
                  每一条拓展流程的句尾标点必须为冒号：
                  
                  要求：
                  1. 重新生成的拓展流程仍应包括type、id、title和content字段，content内容为一个字符串列表
                  2. type必须为Optional、Exception Handling或Selection之一
                  3. id需遵守以上编号编写方法
                  4. title为引发拓展流程的条件说明
                  5. content中，每一步的actor必须是"User"或"System"之一，每一步的action必须是清晰的动作描述
                  6. 返回示例格式：
                  {{
                      "type": "Optional",
                      "id": "*a",
                      "title": "经理 在任意时刻，需要进行超控操作",
                      "content": [
                          "(System) 系统 进入经理授权模式。",
                          "(User) 经理或收银员 执行某一经理模式的操作。",
                          "(System) 系统 回复到收银员授权模式。"
                      ]
                  }}
                    
                  返回JSON格式：{format_instructions}
                """)
        self.chain1 = self.prompt1 | llm | self.parser


    def generate(self, system_desc: str, actor: Dict, user_story: Dict) -> List[dict]:
        """生成完整的基本流程步骤"""
        result = self.chain0.invoke({"system_desc": system_desc, "actor": actor, "user_story": user_story,
                                     "format_instructions": self.parser.get_format_instructions()})
        return result



    def regenerate(self, system_desc: str, actor: Dict, user_story: Dict, old_flow: dict, suggestion: str) -> \
    dict:
        """重新生成步骤"""
        result = self.chain1.invoke(
            {"system_desc": system_desc, "actor": actor, "user_story": user_story, "old_flow": old_flow,
             "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result
