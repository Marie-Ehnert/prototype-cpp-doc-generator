from file_handler import FileHandler
import click

MODELS = {
    "llama3" :"llama3:latest",
    "gemma" : "gemma:7b"
}

#file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
# file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/RationalNumberClassValueSemantics.cpp")
# code = file_handler.read_source_file()
# tree = file_handler.generate_ast_from_source_code(code)

# file_handler.extract_function_definitions(tree)

# @click.command()
# @click.argument("source_file", type=click.Path(exists=True))
# @click.argument("model", type=click.Choice(MODELS))
# def cli(source_file, model):
#     print("hello")
    
@click.command()
@click.option("--name", prompt="Enter name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}")


if __name__ == "__main__":
    hello()