from file_handler import *
from utils.helper_functions import *  
import re

class MetaInfo:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler
        self.code = file_handler.read_source_file()
        self.tree = file_handler.generate_ast_from_source_code(self.code)
        

    # TODO add error handling
    def extract_function(self, node: Node):
        content = node.text.decode("utf-8")
        params = []
        function_type = None
        parent_class = None

        function_type_node = node.child_by_field_name("type")
        if function_type_node:
            function_type = function_type_node.text.decode("utf-8")

        function_header_node = node.child_by_field_name("declarator")
        if not function_type:
            function_header = function_header_node.text.decode("utf8")
        else: function_header = f"{function_type} {function_header_node.text.decode("utf8")}"

        if function_header_node.type == "reference_declarator": #needed since the immediate declarator field name has two fields 1) reference_declarator and 2) function_declarator
            function_identifier_node = function_header_node.child(1).child_by_field_name("declarator") 
            function_identifier = function_identifier_node.text.decode("utf-8")
            functions_parameter_node = function_header_node.child(1).child_by_field_name("parameters")
            if functions_parameter_node:
                for param in functions_parameter_node.children:
                    if param.type == "parameter_declaration":
                        params.append(param.text.decode("utf-8"))
        else: 
            function_identifier_node = function_header_node.child_by_field_name("declarator")
            function_identifier = function_identifier_node.text.decode("utf-8")
            functions_parameter_node = function_header_node.child_by_field_name("parameters")
            if functions_parameter_node:
                for param in functions_parameter_node.children:
                    if param.type == "parameter_declaration":
                        params.append(param.text.decode("utf-8"))

        return (
            "function",
            function_type,
            function_identifier,
            params,
            function_header,
            parent_class,
            node.start_point.row + 1,
            node.end_point.row + 1,
            content,
        )


    def extract_class(self, node: Node):
        attributes = []
        methods = []
        content = node.text.decode("utf-8")
        parent_class = None

        class_name_node = node.child_by_field_name("name")
        class_name = class_name_node.text.decode("utf8")

        if class_name_node.next_sibling.type == "base_class_clause":
            parent_class_node = class_name_node.next_sibling
            for child in parent_class_node.children:
                if child.type == "type_identifier":
                    parent_class = child.text.decode("utf-8")

        class_body_node = node.child_by_field_name("body")
        if class_body_node:
            for child in class_body_node.children:
                if child.type == "function_definition":
                    method = child.child_by_field_name("declarator").text.decode("utf-8")
                    methods.append(method)
                elif child.type == "field_declaration" and child.child_by_field_name("declarator").type == "field_identifier":
                    attribute = child.text.decode("utf-8")
                    attribute_edit = re.sub(r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/","", attribute) #removes multiline comments
                    attribute_edit_all_comments = re.sub(r"\/\/[^\n\r]+?(?:\*\)|[\n\r])", "", attribute_edit) #removes single line comments
                    if "," in attribute_edit_all_comments:
                        multiple_attributes = attribute_edit_all_comments.split(",")
                        for item in multiple_attributes:
                            attributes.append(item.strip())
                    else:
                        attributes.append(attribute_edit_all_comments)
        return (
            "class",
            class_name,
            parent_class,
            attributes,
            methods,
            node.start_point.row + 1,
            node.end_point.row + 1,
            content,
        )

    def add_methods_outside_a_class(self, list: list[dict]):
        for dictionary in list:
            if is_class(dictionary):
                class_info = dictionary["class"]
                name = class_info["class_name"]
                for other_dictionary in list:
                    if is_function(other_dictionary):
                        func_info = other_dictionary["function"]
                        method_name = func_info["identifier"]
                        if f"{name}::" in method_name:
                            class_info["methods"].append(func_info["header"])

    def add_parent_relationship_to_method_definitions_inside_class(self, definitions: list[dict]):
        for function_definition in definitions:
            if is_function(function_definition):
                func_info = function_definition["function"]
                for class_definition in definitions:
                    if "class" in class_definition.keys():
                        class_info = class_definition["class"]
                        if is_function_def_inside_class_def(func_info, class_info):
                            func_info["parent_class"] = class_info["class_name"]
                        
    def add_parent_relationship_to_method_definitions_outside_class(self, definitions: list[dict]):
        for definition in definitions:
            if is_function(definition):
                func_info = definition["function"]
                if "::" in func_info["identifier"]:
                    match = re.findall(r".*(?=::)", func_info["identifier"])
                    func_info["parent_class"] = match[0]

    # Entry point of global analysis
    def extract_definitions(self):
        # A list to store extracted information
        definitions = []
        root_node = self.tree.root_node

        # Function to traverse the AST
        def walk_tree_and_extract(self, node: Node):

            if node.type == "function_definition":
                function_def = self.extract_function(node)
                # Structure of a function tuple: ("function", type, name, [params], full header, parent_class, start line, end line, code content)
                definitions.append(function_def)

            elif node.type == "class_specifier":
                # guard to prevent extraction of class specifier without body
                if node.child_by_field_name("body"):
                    class_def = self.extract_class(node)
                    # Structure of a class tuple: ("class", name, parent_class, [attributes], [inline methods], start line, end line, code content)
                    definitions.append(class_def)

            # Recursively visit all children of the node
            for child in node.children:
                walk_tree_and_extract(self, child)

        # Start walking the tree from the root node
        walk_tree_and_extract(self, root_node)

        # creates python list of dictionaries -> needs to be maintained if new key is added for the extraction
        definitions = definition_tuple_list_to_dict_list(definitions)

        self.add_methods_outside_a_class(definitions)
        self.add_parent_relationship_to_method_definitions_inside_class(definitions)
        self.add_parent_relationship_to_method_definitions_outside_class(definitions)

        return definitions
