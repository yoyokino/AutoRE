from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class BasicFlowAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template(
            """Based on the provided system description, system entity information, actor, and user-story, generate the complete basic flow steps:
            
            System Description:  
            {system_desc}
            
            System Entity Information:  
            {entities}
            
            Actor:  
            {actor}
            
            User Story:  
            {user_story}
            
            Requirements:  
            1. Each step must consist of only a single string.  
            2. The actor must be either "User" or "System".  
            3. Action statements must clearly describe actions being performed.
            4. You must return a list of string, not a dict containing list.  
            5. Example returned format:
            
            [
                "(User) Customer should bring items to POS checkout for purchase.",
                "(User) Cashier should initiate a new sale.",
                "(System) CoCoME should start a new sale.",
                "(User) Cashier should enter item identifier.",
                "(System) While a new sale is active, CoCoME should record each sales item, providing item description and running total. (Repeat steps 4–5 until input ends.)",
                "(System) Upon ending the sale, CoCoME should submit calculated taxes.",
                "(User) Cashier should inform the customer of the total amount and request payment.",
                "(User) Customer should pay the total amount. (Select a8, b8, c8, d8)",
                "(System) After the payment is completed, CoCoME should process the payment.",
                "(System) Once sale completion occurs, CoCoME should record the completed sale, send the data to external accounting and inventory systems, and issue a receipt."
            ]
            
            Return in JSON format: {format_instructions}""")
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template(
            """Based on the existing step and modification suggestions, regenerate the step:
            
            System Description:
            {system_desc}
            
            System Entity Information:
            {entities}
            
            Actor:
            {actor}
            
            Existing User-Story:
            {user_story}
            
            Original Single-Step Basic Flow:
            {old_step}
            
            Modification Suggestions:
            {suggestion}
            
            Requirements:
            1. The returned single step must contain only one field: "new_step".
            2. The "actor" must remain as originally defined in the single-step basic flow ("User" or "System"), without modification.
            3. The "action" must clearly describe an action compatible with the given modification suggestions.
            4. Example of expected returned format:
               {{"new_step": "(User) Customer should arrive at the POS cashier with items ready for purchase."}}
            
            Return in JSON format: {format_instructions}""")
        self.chain1 = self.prompt1 | llm | self.parser

        self.prompt2 = ChatPromptTemplate.from_template(
            """Based on existing steps and modification suggestions, regenerate the steps:
            
            System Description:
            {system_desc}
            
            System Entity Information:
            {entities}
            
            Actor:
            {actor}
            
            Existing User-Story:
            {user_story}
            
            Original Basic Flow Steps:
            {old_steps}
            
            Modification Suggestions:
            {suggestion}
            
            Requirements:
            1. The returned result must be a single list of strings.
            2. Each string must clearly identify an actor as either "User" or "System".
            3. Each string must clearly describe an action consistent with provided modification suggestions.
            4. You must return a list of string, not a dict containing list.
            5. Example returned format:
            [
              "(User) Customer should arrive at the POS cashier with products or services to purchase.",
              "(User) Cashier should initiate a new sale.",
              "(System) CoCoME should start a new sale.",
              "(User) Cashier should enter item identifier.",
              "(System) While a new sale is active, CoCoME should record each sale item and provide item descriptions and running total. (Repeat steps 4-5 until input ends.)",
              "(System) Once the sale ends, CoCoME should submit the total calculated taxes.",
              "(User) Cashier should inform customer of the total amount and request payment.",
              "(User) Customer should pay for the purchase. (Select a8, b8, c8, d8)",
              "(System) After payment completion, CoCoME should process the payment.",
              "(System) Upon completing the sale, CoCoME should record the final sale, send information to external accounting and inventory systems, and generate a receipt."
            ]
            
            Return in JSON format: {format_instructions}""")
        self.chain2 = self.prompt2 | llm | self.parser

    def generate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict) -> List[str]:
        """生成完整的基本流程步骤"""
        result = self.chain0.invoke(
            {"system_desc": system_desc, "entities": entities, "actor": actor, "user_story": user_story,
             "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate_one_step(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict, old_step: str,
                            suggestion: str) -> str:
        """重新生成步骤"""
        result = self.chain1.invoke(
            {"system_desc": system_desc, "entities": entities, "actor": actor, "user_story": user_story,
             "old_step": old_step,
             "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict, old_steps: List[str],
                   suggestion: str) -> \
            List[str]:
        """重新生成步骤"""
        result = self.chain2.invoke(
            {"system_desc": system_desc, "entities": entities, "actor": actor, "user_story": user_story,
             "old_steps": old_steps,
             "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result
