from doc_item import *

class ChatEngine:
    def __init__(self, meta_info: list[dict], model) -> None:
        self.meta_info = meta_info
        self.model = model

    