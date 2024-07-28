from chat_engine import ChatEngine
from file_handler import FileHandler
from meta_info import MetaInfo
from utils.helper_functions import *  
import click
import toml
from doc_item import *

with open("chat_config.toml", "r") as f:
        config = toml.load(f)
        models = config["configured_models"]["large_language_models"]

@click.command()
@click.option("-f","--cpp-file" ,prompt= "Enter a file path", type=click.Path(exists=True), default="/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
@click.option("-m", "--llm", prompt= "Choose a large language model",type=click.Choice(models), default=("deepseek-coder-v2:latest"))
def cli(cpp_file, llm):
    #click library already makes sure that the entered value is a valid file path!
    with open("chat_config.toml", "r") as f:
        config = toml.load(f)
    #sets the model
    config["chat_completion"]["active_model"] = llm
    #retreives the url for the llm api
    host = config["chat_completion"]["base_url"]
    doygen_path = config["doxygen_config"]["doxyfile_path"]
    doxygen_directory_path = config["doxygen_config"]["doxygen_directory_path"]
    #updates the config with the model input
    with open("chat_config.toml", "w") as f:
        toml.dump(config, f)

    try:
        file_handler = FileHandler(cpp_file, doygen_path)
        file_handler.set_up_doxyfile()
        file_handler.run_doxygen()
        meta_info = MetaInfo(file_handler)
        references = meta_info.process_dot_files_in_directory(doxygen_directory_path)
        definitions = meta_info.extract_definitions()
        doc_items = parse_definitions_to_doc_items(definitions)
        add_references_to_doc_items(references, doc_items)
        chat_engine = ChatEngine(doc_items, llm, host, file_handler.file_path)
        chat_engine.attempt_to_generate_documentation()
    except Exception as e:
         handle_exception(e)
        
    # to inspect the extracted code analysis
    # with open("meta.json", "w") as f:
    #     json.dump(definitions, f)

if __name__ == "__main__":
    cli()