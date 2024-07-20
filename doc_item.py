from dataclasses import dataclass, field
from enum import Enum
 
class DocItemType(Enum):
    FUNCTION = "function",
    CLASS = "class"

@dataclass
class DocFunctionItem:
    item_type: DocItemType.FUNCTION = ""
    obj_name: str = ""
    parent_name: str = ""
    parameters: list[str] = field(default_factory=list)
    return_type: str | None = None
    start_line: int = -1
    end_line: int = -1
    content: str = ""

@dataclass
class DocClassItem:
    item_type: DocItemType.CLASS = ""
    obj_name: str = ""
    parent_name: str = ""
    attributes: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    start_line: int = -1
    end_line: int = -1
    content: str = ""

def parse_definitions_to_doc_items(definitions: list[dict]) -> list[DocFunctionItem | DocClassItem]:
    doc_items = []
    for item in definitions:
        if "function" in item.keys():
            function_def = item["function"]
            doc_function_item = DocFunctionItem("function",function_def["identifier"], function_def["parent_class"], function_def["parameters"], function_def["return_type"], function_def["start_line"], function_def["end_line"], function_def["content"])
            print(doc_function_item.obj_name)
            doc_items.append(doc_function_item)
        elif "class" in item.keys():
            class_def = item["class"]
            doc_class_item = DocClassItem("class",class_def["class_name"], class_def["parent_class"], class_def["attributes"], class_def["methods"], class_def["start_line"], class_def["end_line"], class_def["content"])
            print(doc_class_item.obj_name)
            doc_items.append(doc_class_item)
    return doc_items
