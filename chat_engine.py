import datetime
import os
from doc_item import *
import ollama
import tiktoken
from ollama import Client, ResponseError
from prompt import SYS_PROMPT, USR_PROMPT
from tqdm import tqdm


class ChatEngine:
    def __init__(self, doc_items: list[DocClassItem | DocFunctionItem], model: str, host: str, file_location: str) -> None:
        self.doc_items = doc_items
        self.model = model
        self.host = host
        self.max_tokens = self.get_max_tokens_from_model(self.model)
        self.file_location = file_location

    @staticmethod
    def get_max_tokens_from_model(model: str):
        model_info = ollama.show(model)
        context_length_prefix = model_info["details"]["family"]
        model_specific_context_length = context_length_prefix + ".context_length"
        return model_info["model_info"][model_specific_context_length]

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
        #uses a general encoding schema -> not all are supported and for an approximation it shall suffice
        def approximate_token_count(prompt: str):
            encoding = tiktoken.encoding_for_model("gpt2")
            token_count = len(encoding.encode(prompt))
            return token_count
            
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
        
        def create_dynamic_markdown_file_name(source_file: str):
            target_directory = os.path.dirname(source_file)
            now = datetime.datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H:%M:%S")
            doc_name = f"{target_directory}/generated_docs_{dt_string}.md"
            return doc_name

           
        pbar = tqdm(self.doc_items, ncols=150)
        doc_path = create_dynamic_markdown_file_name(self.file_location)
        for item in pbar:
            item_prompt = self.enrich_template_prompt_with_meta_data(item)
            token_count = approximate_token_count(item_prompt)
            pbar.set_description(f"Generating documentation - {item.item_type} {item.obj_name} | token count {token_count}")
            heading = add_markdown_heading(item)
            if token_count <= self.max_tokens:
                try:
                    llm_response = self.send_request_to_llm(item_prompt, USR_PROMPT)
                    with open(doc_path, "a") as f:
                        f.write( heading + llm_response + "\n" + add_markdown_ending())
                except ResponseError:
                    pass
            else:
                if isinstance(item, DocClassItem):
                    print("\nThe token amount is too big for this model - Truncating the code ")
                    truncated_item_prompt = self.enrich_template_prompt_with_meta_data_without_the_code_content(item)
                    truncated_token_count = approximate_token_count(truncated_item_prompt)
                    if truncated_token_count <= self.max_tokens:
                        try:
                            llm_response = self.send_request_to_llm(truncated_item_prompt, USR_PROMPT)
                            with open(doc_path, "a") as f:
                                f.write( heading + llm_response + "\n" + add_markdown_ending())
                        except ResponseError:
                            pass
                    else:
                        print("\nEven after truncating the code content the prompt for this class remains too big")
                else: print("\nThe token amount is too big for this model!")
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
        
    @staticmethod
    def enrich_template_prompt_with_meta_data_without_the_code_content(item: DocClassItem):
       
        methods = "\n".join(item.methods)
        attributes = "\n".join(item.attributes)

        methods_prompt = f"""It also contains following methods:\n{methods}"""
        attributes_prompt = f"""The {item.item_type} {item.obj_name} contains the following attributes:\n{attributes}"""

        prompt_data = {
        "code_type_tell": item.item_type,
        "code_name": item.obj_name,
        "code_content": "The actual code content could not be provided! So please base your assumptions on the following information about the class!",
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