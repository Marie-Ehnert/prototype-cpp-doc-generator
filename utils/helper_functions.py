def append_list_items_to_list(list_1: list, list_2: list):
    for item in list_2:
        list_1.append(item)
    return list_1

def definition_tuple_list_to_dict_list(list: list[tuple]):
    dict_list = []
    for tuple in list:
        dictionary = dict()
        if tuple[0] == "function":
            dictionary["return_type"] = tuple[1]
            dictionary["identifier"] = tuple[2]
            dictionary["parameters"] = tuple[3]
            dictionary["header"] = tuple[4]
            dictionary["start_line"] = tuple[5]
            dictionary["end_line"] = tuple[6]
            dictionary["content"] = tuple[7]
            function_dictionary = dict()
            function_dictionary["function"] = dictionary
            dict_list.append(function_dictionary)
        elif tuple[0] == "class":
            dictionary["class_name"] = tuple[1]
            dictionary["attributes"] = tuple[2]
            dictionary["methods"] = tuple[3]
            dictionary["start_line"] = tuple[4]
            dictionary["end_line"] = tuple[5]
            dictionary["content"] = tuple[6]
            class_dictionary = dict()
            class_dictionary["class"] = dictionary
            dict_list.append(class_dictionary)
    return dict_list