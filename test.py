from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_cpp as tscpp
from utils.helper_functions import definition_tuple_list_to_dict_list
import json
import re

import pydot


parser = Parser(Language(tscpp.language()))

rn_value = "/Users/mehnert/uni-leipzig/sources/RationalNumberClassValueSemantics.cpp"
rn_ref = "/Users/mehnert/uni-leipzig/sources/RationalNumberClassReferenceSemantics.cpp"
ec = "/Users/mehnert/uni-leipzig/sources/ec/EC.cpp"


def dot_to_json(dot_file_path, json_file_path):
    # Parse the .dot file
    graphs = pydot.graph_from_dot_file(dot_file_path)
    graph = graphs[0]

    # Initialize the data structure
    data = {}

    # Extract nodes and initialize the structure
    for node in graph.get_nodes():
        node_name = node.get_name().strip('"')
        node_label = node.get_attributes().get('label', '').strip('"')
        if node_label:
            data[node_label] = {
                'calls': [],
                'called_by': []
            }
        elif node_name:  # Fallback to node name if label is not present
            data[node_name] = {
                'calls': [],
                'called_by': []
            }

    # Extract edges and populate the structure
    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        destination = edge.get_destination().strip('"')
        
        # Resolve the labels for source and destination nodes
        source_label = graph.get_node(source)[0].get_attributes().get('label', '').strip('"')
        destination_label = graph.get_node(destination)[0].get_attributes().get('label', '').strip('"')

        if source_label and destination_label:
            data[source_label]['calls'].append(destination_label)
            data[destination_label]['called_by'].append(source_label)
        elif source and destination:
            data[source]['calls'].append(destination)
            data[destination]['called_by'].append(source)

    # Save to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
dot_file_path = '/Users/mehnert/uni-leipzig/ec_test/doc/html/_e_c_8cpp_ae66f6b31b5ad750f1fe042a706a4e3d4_cgraph.dot'  # Replace with your .dot file path
json_file_path = 'output.json'  # Replace with your desired output path
dot_to_json(dot_file_path, json_file_path)