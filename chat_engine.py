from time import sleep
from venv import logger
from doc_item import *
import ollama
from ollama import Client, ResponseError
from prompt import SYS_PROMPT, USR_PROMPT
from tqdm import tqdm


class ChatEngine:
    def __init__(self, doc_items: list[DocClassItem | DocFunctionItem], model: str, host: str) -> None:
        self.doc_items = doc_items
        self.model = model
        self.host = host

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
        return response_message
    
    def attempt_to_generate_documentation(self):
        # Adds a static heading to generated response
        def add_markdown_heading(item: DocClassItem | DocFunctionItem):
            if isinstance(item, DocFunctionItem) and item.parent_name != "":
                return f"# method {item.obj_name} of {item.parent_name} \n"
            elif isinstance(item, DocFunctionItem) and item.parent_name == "":
                return f"# {item.item_type} {item.obj_name}"
            else: return f"# {item.item_type} {item.obj_name} \n"
        # Adds a divider line to the end of the markdown
        def add_markdown_ending():
            return "***\n"
           
        pbar = tqdm(self.doc_items, ncols=150)
        for item in pbar:
            item_prompt = self.enrich_template_prompt_with_meta_data(item)
            pbar.set_description(f"Generating documentation - {item.item_type} {item.obj_name} ")
            heading = add_markdown_heading(item)
            try:
                llm_response = self.send_request_to_llm(item_prompt, USR_PROMPT)
                with open("docs.md", "a") as f:
                    f.write( heading + llm_response + "\n" + add_markdown_ending())
            except ResponseError as e:
                print("LLM-Backend Error: ", e)
                continue
        print("         --- The Generation of the documentation has been completed! ---")


    @staticmethod
    def enrich_template_prompt_with_meta_data(item: DocClassItem | DocFunctionItem):
        if isinstance(item, DocClassItem):
            methods = "\n".join(item.methods)
            attributes = "\n".join(item.attributes)

            methods_prompt = f"""It also contains following methods:\n{methods}"""
            attributes_prompt = f"""The {item.item_type} {item.obj_name} contains the following attributes:\n{attributes}"""

            prompt_data = {
            "code_type_tell": item.item_type,
            "code_name": item.obj_name,
            "code_content": item.content,
            "actual_parameters_or_attributes": attributes_prompt,
            "methods": methods_prompt,
            "combine_ref_situation": "",
            "have_return_tell": "",
            "has_relationship": "",
            "reference_letter": "",
            "parameters_or_attribute": "attributes",
            }

            sys_prompt = SYS_PROMPT.format(**prompt_data)
            return sys_prompt
        
        elif isinstance(item, DocFunctionItem):
            parameters = "\n".join(item.parameters)

            parameters_prompt = f"""The {item.item_type} {item.obj_name} contains the following parameters:\n{parameters}"""

            prompt_data = {
            "code_type_tell": item.item_type,
            "code_name": item.obj_name,
            "code_content": item.content,
            "actual_parameters_or_attributes": parameters_prompt,
            "methods": "",
            "combine_ref_situation": "",
            "have_return_tell": item.return_type,
            "has_relationship": "",
            "reference_letter": "",
            "parameters_or_attribute": "parameters",
            }

            sys_prompt = SYS_PROMPT.format(**prompt_data)
            return sys_prompt