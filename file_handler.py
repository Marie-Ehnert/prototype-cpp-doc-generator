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
        query_function_definition = self.cpp_language.query(query.alles_zusammen)
        function_definition_info_nodes = query_function_definition.captures(tree.root_node)
        iterator = 0

        while iterator < len(function_definition_info_nodes):
            single_function_def = [function_definition_info_nodes[iterator], function_definition_info_nodes[iterator + 1], function_definition_info_nodes[iterator + 2]]
            function_dto = dict()

            for tuple in single_function_def:
                match tuple:
                    case (_, "name"):
                        function_dto["name"] = tuple[0].text.decode("utf-8")
                    case (_, "param"):
                        params = tuple[0].text.decode("utf-8")[1: -1].split(",")
                        if "" in params:
                            params.remove("")
                        function_dto["params"] = params
                    case (_, "all_lines"):
                        function_dto["content"] = tuple[0].text.decode("utf-8")
                        function_dto["start_line"] = tuple[0].start_point.row + 1
                        function_dto["end_line"] = tuple[0].end_point.row + 1
                        function_dto["type"] = "function_def"
            list.append(function_dto)
            iterator += 3

        return list
    
    def extract_class_definitions(self, tree: Tree) -> list:
        class_list = []
        query_class_definitions = self.cpp_language.query(query.alles_zusammen_klassen)
        query_class_members = self.cpp_language.query(query.alles_zusammen_klassen_ect)
        class_nodes = query_class_definitions.captures(tree.root_node)
        iterator = 0

        while iterator < len(class_nodes):
            single_class_def = [class_nodes[iterator], class_nodes[iterator + 1]]
            class_dto = dict()
            for tuple in single_class_def:
            
                match tuple:
                    case (_,"name"):
                        class_dto["name"] = tuple[0].text.decode("utf-8")
                        class_dto["type"] = "class_def"
                    case (_, "class"):
                        class_dto["start_line"] = tuple[0].start_point.row + 1
                        class_dto["end_line"] = tuple[0].end_point.row + 1
                        class_dto["content"] = tuple[0].text.decode("utf-8")
                        member_nodes = query_class_members.captures(tuple[0])
                        params_list = []

                        for node in member_nodes:
                           params_list.append(node[0].text.decode("utf-8"))
                        class_dto["params"] = params_list
                class_list.append(class_dto)
            iterator += 2
        return class_list
            
