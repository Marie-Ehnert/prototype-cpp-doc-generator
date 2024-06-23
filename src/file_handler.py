import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Tree
import utils.queries as query

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

    def extract_function_definitions(self, tree: Tree) -> list:
        list = []
        query_function_definition = self.cpp_language.query(query.FUNCTION_DEFINITION_IDENTIFIER)
        function_definition_info_nodes = query_function_definition.captures(tree.root_node)
        iterator = 0

        while iterator < len(function_definition_info_nodes):
            single_function_def = [function_definition_info_nodes[iterator], function_definition_info_nodes[iterator + 1]]
            function_dto = dict()

            for tuple in single_function_def:
                match tuple:
                    case (_, "name"):
                        function_dto["name"] = tuple[0].text.decode("utf-8")
                    case (_, "param"):
                        function_dto["params"] = tuple[0].text.decode("utf-8")[1: -1].split(",")

            list.append(function_dto)
            iterator += 2

        print(list)
        return list
