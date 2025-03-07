from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class UserStoryAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template(
            """Based on the system description, actor list, and the specified actor and actor description, generate a list of User-Stories for the specified actor:
            
            System Description:
            {system_desc}
            
            Actor List:
            {actors}
            
            Specified Actor:
            {actor}
            
            Requirements:
            1. Each User-Story must contain only a single field "user_story", expressed clearly and concisely in one sentence, following the standard User-Story format.
            2. Each User-Story must relate specifically to the specified actor.
            3. Example of expected format:
               [{{"user_story": "As a cashier, I want to process item checkout so that the customer can pay, completing the purchase and enabling the system to record the transaction."}}, ...]
            
            Return in JSON format: {format_instructions}""")  # 修正处：使用双大括号转义示例中的JSON符号
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template(
            """Based on the system description, actor list, the specific actor and its description, an original User-Story, and the client's modification suggestions, regenerate a modified version of this User-Story:
            
            System Description:
            {system_desc}
            
            Actor List:
            {actors}
            
            Specific Actor:
            {actor}
            
            Original User-Story:
            {old_user_story}
            
            Client's Modification Suggestions:
            {suggestion}
            
            Requirements:
            1. Example of expected returned format:
               {{"user_story": "As a cashier, I want to process item checkout so that the customer can pay to complete the shopping and the system can record the transaction."}}
            2. The regenerated User-Story must contain only one field ("user_story"), expressed clearly and concisely in one sentence as a requirement in the form of a User-Story.
            
            Return in JSON format: {format_instructions}""")  # 修正处：使用双大括号转义示例中的JSON符号
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
