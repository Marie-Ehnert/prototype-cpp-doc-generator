from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_cpp as tscpp
from utils.helper_functions import definition_tuple_list_to_dict_list
import json


parser = Parser(Language(tscpp.language()))

rn_value = "/Users/mehnert/uni-leipzig/sources/RationalNumberClassValueSemantics.cpp"
ec = "/Users/mehnert/uni-leipzig/sources/ec/EC.cpp"



# TODO add error handling
def extract_function(node: Node):
    content = node.text.decode("utf-8")
    params = []
    function_type = None

    function_type_node = node.child_by_field_name("type")
    if function_type_node:
        function_type = function_type_node.text.decode("utf-8")

    function_header_node = node.child_by_field_name("declarator")
    function_header = function_header_node.text.decode("utf8")

    if function_header_node.type == "reference_declarator":
        function_identifier_node = function_header_node.child(1).child_by_field_name("declarator")
        function_identifier = function_identifier_node.text.decode("utf-8")
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
        node.start_point.row + 1,
        node.end_point.row + 1,
        content,
    )


def extract_class(node: Node):
    attributes = []
    methods = []
    content = node.text.decode("utf-8")

    class_name_node = node.child_by_field_name("name")
    class_name = class_name_node.text.decode("utf8")

    class_body_node = node.child_by_field_name("body")
    if class_body_node:
        for child in class_body_node.children:
            if child.type == "function_definition":
                method = child.child_by_field_name("declarator").text.decode("utf-8")
                methods.append(method)
            elif child.type == "field_declaration" and child.child_by_field_name("declarator").type == "field_identifier":
                attribute = child.text.decode("utf-8")
                if "," in attribute:
                    multiple_attributes = attribute.split(",")
                    for item in multiple_attributes:
                        attributes.append(item.strip())
                else:
                    attributes.append(attribute)
    return (
        "class",
        class_name,
        attributes,
        methods,
        node.start_point.row + 1,
        node.end_point.row + 1,
        content,
    )


def extract_definitions():
    source_code_file = open(ec, "r", encoding="utf-8")
    code = source_code_file.read()
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node  

    # A list to store extracted information
    definitions = []

    # Function to traverse the AST
    def walk_tree_and_extract(node: Node):

        if node.type == "function_definition":
            function_def = extract_function(node)
            # Structure of a function tuple: ("function", type, name, [params], full header, start line, end line, code content)
            definitions.append(function_def)

        elif node.type == "class_specifier":
            # guard to prevent extraction of class specifier without body
            if node.child_by_field_name("body"):
                class_def = extract_class(node)
                # Structure of a class tuple: ("class", name, [attributes], [inline methods], start line, end line, code content)
                definitions.append(class_def)

        # Recursively visit all children of the node
        for child in node.children:
            walk_tree_and_extract(child)

    # Start walking the tree from the root node
    walk_tree_and_extract(root_node)

    return definitions


definitions = extract_definitions()
please = definition_tuple_list_to_dict_list(definitions)

with open("meta.json", "w") as f:
    json.dump(please, f)
