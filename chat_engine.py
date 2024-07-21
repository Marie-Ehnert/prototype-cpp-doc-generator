from doc_item import *
from ollama import Client

class ChatEngine:
    def __init__(self, doc_items: list[DocClassItem | DocFunctionItem], model: str, host: str) -> None:
        self.doc_items = doc_items
        self.model = model
        self.host = host

    #TODO prompt vorbereitung 

    def send_request_to_llm(self, sys_prompt, usr_prompt):
        client = Client(host= self.host)
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]

        response = client.chat(
            model= self.model,
            messages=messages
        )

        response_message = response['message']['content']
        print(response_message)
        return response_message

    @staticmethod
    def enrich_template_prompt_with_meta_data(item: DocClassItem | DocFunctionItem):
        if isinstance(item, DocClassItem):
            attributes = item.attributes
            methods = item.methods
            
            attributes_and_methods = f""""""

            prompt_data = {
            "code_type_tell": item.item_type,
            "code_name": item.obj_name,
            "code_content": item.content,
            "have_return_tell": "",
            "has_relationship": "",
            "reference_letter": reference_letter,
            "referencer_content": referencer_content,
            "parameters_or_attribute": parameters_or_attribute,
            }
        elif isinstance(item, DocFunctionItem):
            return False