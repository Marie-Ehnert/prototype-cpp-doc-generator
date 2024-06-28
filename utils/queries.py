FUNCTION_DEFINITION_IDENTIFIER_AND_CONSTRUCTORS = "(function_definition declarator: (function_declarator declarator: (identifier) @name parameters: (parameter_list) @param))"

MEMBER_FUNCTION_DEFINITION_OUTSIDE = "(function_definition declarator: (function_declarator declarator: (qualified_identifier) @name parameters: (parameter_list) @param))"

MEMBER_FUNCTION_DEFINITION_INSIDE = "((function_definition declarator: (reference_declarator (function_declarator declarator: (field_identifier) @name parameters: (parameter_list) @params))) @header_and_body"

alles_zusammen ="""
(function_definition declarator: [
    (function_declarator declarator: (identifier) @name parameters: (parameter_list) @param)
    (function_declarator declarator: (field_identifier) @name parameters: (parameter_list) @param)
    (function_declarator declarator: (qualified_identifier) @name parameters: (parameter_list) @param)
    (reference_declarator (function_declarator declarator: (qualified_identifier) @name parameters: (parameter_list) @param))
    (reference_declarator (function_declarator declarator: (field_identifier) @name parameters: (parameter_list) @param)) 
]) @all_lines
"""

alles_zusammen_klassen ="""
(class_specifier name: (type_identifier) @name body: (field_declaration_list (field_declaration type: (_)@type declarator: (field_identifier) @var ))) @all_lines
"""