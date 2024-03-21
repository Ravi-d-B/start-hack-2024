import streamlit as st
import graphviz
import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional

SIZE = '40,40'

LEVEL_1_COLOUR = '#f4b484'
LEVEL_2_COLOUR = '#a8c98c'
LEVEL_3_COLOUR = '#fa640c'
LEVEL_4_COLOUR = '#fada63'
UNTESTED = '#f0f0f0'

LEVEL_1_COLOUR_LIGHT = '#d39e76'
LEVEL_2_COLOUR_LIGHT = '#92b278'
LEVEL_3_COLOUR_LIGHT = '#c9520a'
LEVEL_4_COLOUR_LIGHT = '#c6b853'
UNTESTED_LIGHT = '#d8d8d8'


def add_node_for_level(graph, node_name, node_label, level: Optional[int]):
    if level == 1:
        add_node(graph, node_name, node_label, LEVEL_1_COLOUR, LEVEL_1_COLOUR_LIGHT)
    elif level == 2:
        add_node(graph, node_name, node_label, LEVEL_2_COLOUR, LEVEL_2_COLOUR_LIGHT)
    elif level == 3:
        add_node(graph, node_name, node_label, LEVEL_3_COLOUR, LEVEL_3_COLOUR_LIGHT)
    elif level == 4:
        add_node(graph, node_name, node_label, LEVEL_4_COLOUR, LEVEL_4_COLOUR_LIGHT)
    else:
        add_node(graph, node_name, node_label, UNTESTED, UNTESTED_LIGHT)


def add_node(graph, node_name, node_label, node_colour, border_colour):
    graph.node(node_name,
               node_label,
               style='filled',
               fillcolor=node_colour,
               color=border_colour,
               penwidth='2'
               )


def add_edge_with_color(graph, from_node, to_node, level: Optional[int]):
    # Choose edge color based on the level of the destination node
    if level == 1:
        edge_color = LEVEL_1_COLOUR_LIGHT
    elif level == 2:
        edge_color = LEVEL_2_COLOUR_LIGHT
    elif level == 3:
        edge_color = LEVEL_3_COLOUR_LIGHT
    elif level == 4:
        edge_color = LEVEL_4_COLOUR_LIGHT
    else:
        edge_color = UNTESTED_LIGHT

    graph.edge(from_node, to_node, color=edge_color, penwidth='1')

def create_graph(levels):
    # Create a graphlib graph object
    graph = graphviz.Digraph()
    graph.attr(size=SIZE)
    graph.attr(rankdir='TB')  # Left to Right direction

    # Basic Number Concepts
    add_node_for_level(graph, 'A', 'Read and Write \n Numbers up to 10', level=levels[0])
    add_node_for_level(graph, 'B', 'Read and Write \n Numbers 10 to 100', level=levels[1])
    add_node_for_level(graph, 'C', 'Plus Symbol +', level=levels[2])
    add_node_for_level(graph, 'D', 'Minus Symbol -', level=levels[3])
    add_node_for_level(graph, 'E', 'Equal Symbol =', level=levels[4])

    # Layer 2
    add_node_for_level(graph, 'F', 'Even, Odd Numbers', level=levels[5])
    add_node_for_level(graph, 'G', 'Greater Than, Smaller \n Than, Symbols <, >', level=levels[6])

    add_edge_with_color(graph, 'A', 'B', level=levels[1])
    add_edge_with_color(graph, 'A', 'C', level=levels[2])
    add_edge_with_color(graph, 'A', 'D', level=levels[3])
    add_edge_with_color(graph, 'A', 'E', level=levels[4])

    add_edge_with_color(graph, 'B', 'F', level=levels[5])
    add_edge_with_color(graph, 'C', 'G', level=levels[6])
    add_edge_with_color(graph, 'D', 'G', level=levels[6])
    add_edge_with_color(graph, 'E', 'G', level=levels[6])

    return graph


levels =[None] * 7
graph = create_graph(levels)
st.graphviz_chart(graph, use_container_width=True)

levels = [4,3,2,1,1,1,None]
graph1 = create_graph(levels)
st.graphviz_chart(graph1, use_container_width=True)


levels = [4,4,4,4,4,3,3]
graph2 = create_graph(levels)
st.graphviz_chart(graph2, use_container_width=True)