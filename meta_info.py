from file_handler import *
import json

class MetaInfo:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler
        self.code = file_handler.read_source_file()
        
    def add_parent_relationships(self):
        tree = self.file_handler.generate_ast_from_source_code(self.code)

        functions = self.file_handler.extract_function_definitions(tree)
        classes = self.file_handler.extract_class_definitions(tree)

        for class_def in classes:
            class_def["methods"] = []
            for function_def in functions:
                if function_def["start_line"] > class_def["start_line"] and function_def["end_line"] < class_def["end_line"]:
                    class_def["methods"].append(function_def["name"])
        
        test = {}
        test = classes
        with open("meta.json", "w") as f:
            json.dump(test,f)