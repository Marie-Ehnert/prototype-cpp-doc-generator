import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Tree


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_source_file(self) -> str:
        source_code_file = open(self.file_path, "r", encoding="utf-8")
        return source_code_file.read()

    def generate_ast_from_source_code(self, source_code: str) -> Tree:
        cpp_language = Language(tscpp.language())
        parser = Parser(cpp_language)
        tree = parser.parse(bytes(source_code, "utf8"))
        return tree

    def extract_function_and_class_definitions(self, tree: Tree) -> list:
        list = []
        for node in tree.root_node.children:
            if node.type == "function_definition" or node.type == "class_specifier":
                type = node.type
                name = node.field_name_for_child
                params = (
                    [arg.arg for arg in node.args.args] if "args" in dir(node) else []
                )
                start_line = node.start_point
                end_line = node.end_point
                list.append((type, name, params, start_line, end_line))
        return list
