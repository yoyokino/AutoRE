from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ConditionAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()

        # 生成前后置条件的prompt
        self.prompt0 = ChatPromptTemplate.from_template(
            """Based on the system description, system entity information, actors and their descriptions, and the given User-Story, generate the Pre-/Post-Conditions for this User-Story:
            
            System Description:
            {system_desc}
            
            System Entity Information:
            {entities}
            
            Actor:
            {actor}
            
            User-Story:
            {user_story}
            
            Requirements:  
            1. Must include two fields: "pre_condition" and "post_condition".  
            2. Conditions must be expressed clearly in short declarative statements. Both "pre_condition" and "post_condition" should contain only one string each. Each string may contain multiple sentences, but they must not be expressed as a list.  
            3. Example of expected returned format:  
               {{"pre_condition": "User has logged into the system.", "post_condition": "Checkout information has been saved to the database. Inventory information has been updated in the database."}}
            
            Return in JSON format: {format_instructions}""")
        self.chain0 = self.prompt0 | llm | self.parser

        # 重新生成单个条件的prompt 
        self.prompt1 = ChatPromptTemplate.from_template(
            """Based on the system description, system entity information, actor list, actor and its description, User-Story, original conditions, and modification suggestions, regenerate the conditions:
            
            System Description:  
            {system_desc}  
            
            System Entity Information:  
            {entities}  
            
            User-Story:  
            {user_story}  
            
            Original Conditions:  
            {old_condition}  
            
            Modification Suggestions:  
            {suggestion}  
            
            Requirements:
            1. Regenerate two corresponding fields according to the two condition types ("pre_condition" and "post_condition").
            2. Conditions must be expressed in clear, concise declarative statements. Both the "pre_condition" and "post_condition" fields must contain only one string. Multiple sentences are allowed within each string, but lists are not permitted.
            3. Example of expected returned format:
               {{"pre_condition": "User has logged into the system.", "post_condition": "Checkout information has been saved to the database. Inventory information has been updated in the database."}}
            
            Return in JSON format: {format_instructions}""")
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
