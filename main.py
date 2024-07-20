from chat_engine import ChatEngine
from file_handler import FileHandler
from meta_info import MetaInfo
from utils.helper_functions import *  
import click
import json
import toml
from doc_item import *

MODELS = {
    "llama3" :"llama3:latest",
    "gemma" : "gemma:7b"
}

#file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
# file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/RationalNumberClassValueSemantics.cpp")
# code = file_handler.read_source_file()
# tree = file_handler.generate_ast_from_source_code(code)

# file_handler.extract_function_definitions(tree)

@click.command()
@click.option("-f","--cpp-file" ,prompt= "Enter a file path", type=click.Path(exists=True), default="/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
@click.option("-m", "--llm", prompt= "Choose a large language model",type=click.Choice(MODELS), default=("gemma"))
def cli(cpp_file, llm):

    #updates config file with model input
    with open("chat_config.toml", "r") as f:
        config = toml.load(f)
    
    config["chat_completion"]["model"] = llm

    with open("chat_config.toml", "w") as f:
        toml.dump(config, f)

    file_handler = FileHandler(cpp_file)
    meta_info = MetaInfo(file_handler)
    definitions = meta_info.extract_definitions()
    doc_items = parse_definitions_to_doc_items(definitions)
    chat_engine = ChatEngine(doc_items, llm)
    chat_engine.send_request_to_llm()


    # with open("meta.json", "w") as f:
    #     json.dump(definitions, f)

if __name__ == "__main__":
    cli()