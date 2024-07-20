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
class DocFunctionClass:
    item_type: DocItemType.CLASS = ""
    obj_name: str = ""
    parent_name: str = ""
    attributes: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    start_line: int = -1
    end_line: int = -1
    content: str = ""

