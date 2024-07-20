from doc_item import *
from ollama import Client

class ChatEngine:
    def __init__(self, doc_items: list[DocClassItem | DocFunctionItem], model) -> None:
        self.doc_items = doc_items
        self.model = model

    #TODO prompt vorbereitung 

    def send_request_to_llm(self):
        client = Client(host='http://localhost:11434')
        response = client.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
        ])
        print(response)