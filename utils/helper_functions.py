def append_list_items_to_list(list_1: list, list_2: list):
    for item in list_2:
        list_1.append(item)
    return list_1

def definition_tuple_list_to_dict_list(list: list[tuple]) -> list[dict]:
    dict_list = []
    for tuple in list:
        dictionary = dict()
        if tuple[0] == "function":
            dictionary["return_type"] = tuple[1]
            dictionary["identifier"] = tuple[2]
            dictionary["parameters"] = tuple[3]
            dictionary["header"] = tuple[4]
            dictionary["parent_class"] = tuple[5]
            dictionary["start_line"] = tuple[6]
            dictionary["end_line"] = tuple[7]
            dictionary["content"] = tuple[8]
            function_dictionary = dict()
            function_dictionary["function"] = dictionary
            dict_list.append(function_dictionary)
        elif tuple[0] == "class":
            dictionary["class_name"] = tuple[1]
            dictionary["parent_class"] = tuple[2]
            dictionary["attributes"] = tuple[3]
            dictionary["methods"] = tuple[4]
            dictionary["start_line"] = tuple[5]
            dictionary["end_line"] = tuple[6]
            dictionary["content"] = tuple[7]
            class_dictionary = dict()
            class_dictionary["class"] = dictionary
            dict_list.append(class_dictionary)
    return dict_list

def is_class(definition: dict) -> bool:
    return "class" in definition.keys()

def is_function(definition: dict) -> bool:
    return "function" in definition.keys()

def is_function_def_inside_class_def(function_def: dict, class_def: dict) -> bool:
    return (function_def["start_line"] > class_def["start_line"] and function_def["end_line"] < class_def["end_line"])