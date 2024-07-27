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
    callers: list = field(default_factory=list)
    callees: list = field(default_factory=list)

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
            doc_items.append(doc_function_item)
        elif "class" in item.keys():
            class_def = item["class"]
            doc_class_item = DocClassItem("class",class_def["class_name"], class_def["parent_class"], class_def["attributes"], class_def["methods"], class_def["start_line"], class_def["end_line"], class_def["content"])
            doc_items.append(doc_class_item)
    return doc_items

def add_references_to_doc_items(objects_with_callers_callees: dict, doc_items_without_references: list[DocFunctionItem | DocClassItem]):
    for item in doc_items_without_references:
        if isinstance(item, DocFunctionItem):
            if f"{item.parent_name}::" in item.obj_name:
                for object in objects_with_callers_callees:
                     if item.obj_name == object:
                         callers_callees = objects_with_callers_callees.get(f"{object}")
                         item.callers = callers_callees.get("callers")
                         item.callees = callers_callees.get("callees")
            elif item.parent_name == None:
                for object in objects_with_callers_callees:
                     if item.obj_name == object:
                         callers_callees = objects_with_callers_callees.get(f"{object}")
                         item.callers = callers_callees.get("callers")
                         item.callees = callers_callees.get("callees")
            elif item.parent_name != None:
                for object in objects_with_callers_callees:
                     if f"{item.parent_name}::{item.obj_name}" == object:
                         callers_callees = objects_with_callers_callees.get(f"{object}")
                         item.callers = callers_callees.get("callers")
                         item.callees = callers_callees.get("callees")
                
