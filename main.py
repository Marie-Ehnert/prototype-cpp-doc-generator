from chat_engine import ChatEngine
from file_handler import FileHandler
from meta_info import MetaInfo
from utils.helper_functions import *  
import click
import json
import toml
from doc_item import *
from prompt import USR_PROMPT

MODELS = ["llama3", "gemma:7b", "deepseek-coder-v2:latest"]

#file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
# file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/RationalNumberClassValueSemantics.cpp")
# code = file_handler.read_source_file()
# tree = file_handler.generate_ast_from_source_code(code)

# file_handler.extract_function_definitions(tree)

@click.command()
@click.option("-f","--cpp-file" ,prompt= "Enter a file path", type=click.Path(exists=True), default="/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
@click.option("-m", "--llm", prompt= "Choose a large language model",type=click.Choice(MODELS), default=("deepseek-coder-v2:latest"))
def cli(cpp_file, llm):

    #updates config file with model input
    with open("chat_config.toml", "r") as f:
        config = toml.load(f)
    
    config["chat_completion"]["model"] = llm

    host = config["chat_completion"]["base_url"]

    with open("chat_config.toml", "w") as f:
        toml.dump(config, f)

    file_handler = FileHandler(cpp_file)
    meta_info = MetaInfo(file_handler)
    definitions = meta_info.extract_definitions()
    doc_items = parse_definitions_to_doc_items(definitions)
    chat_engine = ChatEngine(doc_items, llm, host)

    prompt = chat_engine.enrich_template_prompt_with_meta_data(doc_items[2])
    #chat_engine.send_request_to_llm(prompt, USR_PROMPT)
    chat_engine.attempt_to_generate_documentation()

    # with open("meta.json", "w") as f:
    #     json.dump(definitions, f)

if __name__ == "__main__":
    cli()