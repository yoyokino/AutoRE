from typing import Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class ExtendedFlowAgent:
    def __init__(self, llm):
        self.parser = JsonOutputParser()
        self.prompt0 = ChatPromptTemplate.from_template(
            """Based on the given system description, entity information, actor, and user story, generate the complete set of Extended Flow steps:
            
            System Description:
            {system_desc}
            
            System Entity Information:
            {entities}
            
            Actor:
            {actor}
            
            User-Story:
            {user_story}
            
            Extended Flow Example:
            
            (Optional) *a, The manager needs to perform override operations at any time:
              1. (System) System enters manager-authorized mode.
              2. (User) Manager or cashier performs an operation requiring manager mode.
              3. (System) System returns to cashier-authorized mode.
            
            (Exception Handling) *b, The system fails at any time:
              1. (User) Cashier restarts the system, logs in, and requests a recovery of the previous state.  
              2. (System) System recovers to the previous state.
            
            (Optional) 2-3a, Customer informs cashier of tax-exempt status (e.g., senior citizen, local resident):
              1. (User) Cashier verifies and enters the tax-exempt status code.
              2. (System) System records the tax-exempt status code (used when calculating tax).
            
            (Selection) 4a, Cash payment:
              1. (User) Cashier enters the received cash amount.
              2. (System) System displays the change amount and opens the cash drawer.
              3. (User) Cashier puts the cash received into drawer and gives the customer change.
              4. (System) System records the cash transaction.
            
            (Selection) 4b, Credit card payment:
              1. (User) Customer enters credit card details.
              2. (System) System displays payment information for verification.
              3. (User) Cashier confirms.
            
            Explanation of Extended Flow Format:
            The above example is a template illustrating the structure of Extended Flows. Each extended flow begins with a property tag: (Optional), (Exception Handling), or (Selection), indicating the type of the extended flow.
            
            - (Optional): other possible events occurring within the basic flow.
            - (Exception Handling): possible exceptional situations occurring within the basic flow.
            - (Selection): options to choose from within the basic flow.
            
            Following the property tag is an identifier representing when this extended flow happens. Identifier formats:  
            - (* + lower-case letter): events occurring at any time.
            - (number + lower-case letter): events occurring at step number N of basic flow.
            - (number-number + lower-case letter): events occurring between steps M and N (inclusive) in the basic flow.
            (Letters are only used for ordering; no sequential meaning is implied.)
            
            Every extended flow title must end with a colon ":".
            
            Requirements:
            1. Each Extended Flow must include "type", "id", "title", and "content", where "content" is a list of strings.
            2. "type" must be one of: "Optional", "Exception Handling", or "Selection".
            3. "id" must strictly follow the formatting rules mentioned above.
            4. "title" must clearly specify the condition triggering the Extended Flow.
            5. In "content", each step must start with "(User)" or "(System)" and clearly describe the action.
            6. You must return a list of dict, not a dict containing list.
            7. Example of expected returned format:
            [
                {{
                    "type": "Optional",
                    "id": "*a",
                    "title": "Manager needs to perform override operations at any time:",
                    "content": [
                        "(System) System enters manager-authorized mode.",
                        "(User) Manager or cashier performs an operation requiring manager mode.",
                        "(System) System returns to cashier-authorized mode."
                    ]
                }},
                {{
                    "type": "Exception Handling",
                    "id": "*b",
                    "title": "System crashes at any time:",
                    "content": [
                        "(User) Cashier restarts the system, logs in, and requests recovery of previous state.",
                        "(System) System recovers to the previous state."
                    ]
                }},
                {{
                    "type": "Selection",
                    "id": "4a",
                    "title": "Cash Payment:",
                    "content": [
                        "(User) Cashier enters the received cash amount.",
                        "(System) System displays change amount and opens cash drawer.",
                        "(User) Cashier puts the received cash in drawer and gives the customer change.",
                        "(System) System records the cash transaction."
                    ]
                }}
                ...
            ]
            
            Return in JSON format: {format_instructions}""")
        self.chain0 = self.prompt0 | llm | self.parser

        self.prompt1 = ChatPromptTemplate.from_template(
            """Based on the given user story and modification suggestions, regenerate one Extended Flow:
            
            System Description:  
            {system_desc}  
            
            System Entity Information:  
            {entities}  
            
            Actor:  
            {actor}  
            
            Current User Story:  
            {user_story}  
            
            Original Extended Flow:  
            {old_flow}  
            
            Modification Suggestions:  
            {suggestion}  
            
            Extended Flow Example:
            (Optional) *a, Manager needs to perform override operations at any time:
              1. (System) System enters manager-authorized mode.
              2. (User) Manager or cashier performs an operation requiring manager mode.
              3. (System) System returns to cashier-authorized mode.
            
            (Exception Handling) *b, System fails at any time:
              1. (User) Cashier restarts the system, logs in, and requests recovery of previous state.
              2. (System) System recovers to the previous state.
            
            (Optional) 2-3a, Customer informs cashier of tax-exempt status (e.g., senior citizen, local resident):
              1. (User) Cashier verifies and enters tax-exempt status code.
              2. (System) System records the tax-exempt status code (used when calculating tax).
            
            (Selection) 4a, Cash payment:
              1. (User) Cashier enters the received cash amount.
              2. (System) System displays change amount and opens cash drawer.
              3. (User) Cashier puts the received cash in the drawer and gives the customer change.
              4. (System) System records the cash transaction.
            
            (Selection) 4b, Credit card payment:
              1. (User) Customer enters credit card details.
              2. (System) System displays payment information for verification.
              3. (User) Cashier confirms.
            
            Explanation of Extended Flow Format:
            Above is the template for the extended flow. Each Extended Flow starts with a type indicator (Optional), (Exception Handling), or (Selection):
            
            - (Optional): Indicates other events that may occur within the basic flow.
            - (Exception Handling): Indicates exceptions that may occur within the basic flow.
            - (Selection): Indicates alternative choices within the basic flow.
            
            The type indicator is followed by an identifier (id), structured as below:
            - (* + lowercase letter): indicates events occurring at any time (the letters are purely labels without sequential meaning).
            - (number + lowercase letter): indicates the event occurs at step N of the basic flow (letters are purely labels without sequential meaning).
            - (number-number + lowercase letter): indicates the event occurs between steps M–N of the basic flow (letters are purely labels without sequential meaning).
            
            Every Extended Flow title must end with a colon (":").
            
            Requirements:
            1. The regenerated Extended Flow must include "type", "id", "title", and "content" fields; "content" is a list of strings.
            2. "type" must be exactly one of "Optional", "Exception Handling", or "Selection".
            3. "id" must follow the identifier guidelines defined above.
            4. "title" must clearly indicate the condition triggering this Extended Flow.
            5. Each step inside "content" must clearly begin with "(User)" or "(System)" and contain a clear action description.
            6. Example of returned format:
            {{
                "type": "Optional",
                "id": "*a",
                "title": "Manager needs to perform override operations at any time:",
                "content": [
                    "(System) System enters manager-authorized mode.",
                    "(User) Manager or cashier performs an operation requiring manager mode.",
                    "(System) System returns to cashier-authorized mode."
                ]
            }}
            
            Return in JSON format: {format_instructions}""")
        self.chain1 = self.prompt1 | llm | self.parser

    def generate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict) -> List[dict]:
        """生成完整的基本流程步骤"""
        result = self.chain0.invoke(
            {"system_desc": system_desc, "entities": entities, "actor": actor, "user_story": user_story,
             "format_instructions": self.parser.get_format_instructions()})
        return result

    def regenerate(self, system_desc: str, entities: List[dict], actor: Dict, user_story: Dict, old_flow: dict,
                   suggestion: str) -> \
            dict:
        """重新生成步骤"""
        result = self.chain1.invoke(
            {"system_desc": system_desc, "entities": entities, "actor": actor, "user_story": user_story,
             "old_flow": old_flow,
             "suggestion": suggestion,
             "format_instructions": self.parser.get_format_instructions()})
        return result
