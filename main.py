from file_handler import FileHandler
from meta_info import MetaInfo
from utils.helper_functions import *  
import click
import json

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
    file_handler = FileHandler(cpp_file)
    # code = file_handler.read_source_file()
    # tree = file_handler.generate_ast_from_source_code(code)
    # functions = file_handler.extract_function_definitions(tree)
    # classes = file_handler.extract_class_definitions(tree)
    # classes_and_functions = append_list_items_to_list(classes, functions)
    # test = {}
    # test = classes_and_functions
    # with open("code.json", "w") as f:
    #     json.dump(test,f)

    meta_info = MetaInfo(file_handler)
    meta_info.add_parent_relationships()

if __name__ == "__main__":
    cli()