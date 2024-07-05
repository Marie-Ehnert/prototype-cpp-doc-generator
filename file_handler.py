import tree_sitter_cpp as tscpp
from tree_sitter import Language, Node, Parser, Tree, TreeCursor

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cpp_language = Language(tscpp.language())

    def read_source_file(self) -> str:
        source_code_file = open(self.file_path, "r", encoding="utf-8")
        return source_code_file.read()

    def generate_ast_from_source_code(self, source_code: str) -> Tree:
        parser = Parser(self.cpp_language)
        tree = parser.parse(bytes(source_code, "utf8"))
        return tree

            
