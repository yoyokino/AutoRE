from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class QualityCheckerAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template("""
                  请根据需求质量属性（必要性、无歧义、一致性、完整性、单一性、可行性、可追溯性、可验证性，来自ISO-29148 单一需求的属性）的要求，检查下列需求文档要素内容的质量，并给出通过与否的反馈：
                  需求文档要素内容（可能是用户故事/用户故事的基本流程/用户故事的拓展流程）：
                  {content}

                  要求：
                  1. 反馈的内容包括result字段与reason字段
                  2. result字段为通过与否的bool类型，只能为true或false
                  3. reason字段为判断的理由
                  4. 返回示例格式：
                     
                  {{
                      "result": "false",
                      "reason": "该需求文档要素在内容上违背了需求单一性，具体......"
                  }}
                  
                  {{
                      "result": "true",
                      "reason": "该需求文档要素在内容上满足所有需求质量属性要求"
                  }}

                  返回JSON格式：{format_instructions}
                """)
        self.chain0 = self.prompt0 | llm | self.parser

    def check(self, content: dict) -> dict:
        """检查质量"""
        result = self.chain0.invoke({"content": content,
                                     "format_instructions": self.parser.get_format_instructions()})
        print(result)
        return result

