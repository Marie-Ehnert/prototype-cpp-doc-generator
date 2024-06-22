from file_handler import FileHandler

print("Hello World")

file_handler = FileHandler("/Users/mehnert/uni-leipzig/sources/ec/EC.cpp")
code = file_handler.read_source_file()
tree = file_handler.generate_ast_from_source_code(code)

print(file_handler.extract_function_and_class_definitions(tree))
