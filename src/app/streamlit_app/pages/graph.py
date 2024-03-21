import streamlit as st
import graphviz
import matplotlib.pyplot as plt
import networkx as nx


# Create a graphlib graph object
graph = graphviz.Digraph()
graph.attr(size='24,24')
graph.attr(rankdir='LR')  # Left to Right direction

# Basic Number Concepts
graph.node('A', 'Read and Write Numbers up to 100', style='filled', fillcolor='lightblue')

# Arithmetic Operations
graph.node('B', 'Plus and Symbol +', style='filled', fillcolor='green')
graph.node('C', 'Minus and Symbol -', style='filled', fillcolor='orange')
graph.node('D', 'Times and Symbol ·', style='filled', fillcolor='green')

# Comparisons and Relations
graph.node('E', 'Greater Than, Smaller Than, Symbols <, >', style='filled', fillcolor='lightyellow')
graph.node('F', 'Even, Odd Numbers', style='filled', fillcolor='lightyellow')

# Advanced Operations and Concepts
graph.node('G', 'Halve, Double', style='filled', fillcolor='lightcoral')
graph.node('H', 'Equal and Symbol =', style='filled', fillcolor='lightcoral')

# Dependencies
graph.edges([('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'E'), ('A', 'F')])
graph.edges([('B', 'G'), ('C', 'G'), ('D', 'G'), ('B', 'H'), ('C', 'H'), ('D', 'H')])



st.graphviz_chart(graph, use_container_width=False)


# Function to create the education graph with detailed objectives
def create_education_graph():
    # Initialize the graph
    graph = graphviz.Digraph('G', filename='education_graph.gv')
    graph.attr(rankdir='LR')  # Left to Right direction
    
    # Node for the foundational concept
    graph.node('1', 'Number and Variable', style='filled', fillcolor='lightblue')
    
    # Nodes for main categories
    graph.node('A', 'A | Operate and Name', style='filled', fillcolor='lightgreen')
    graph.node('B', 'B | Exploring and Arguing', style='filled', fillcolor='lightyellow')
    graph.node('C', 'C | Mathematize and Present', style='filled', fillcolor='lightcoral')
    
    # Sub-nodes for 'Operate and Name'
    graph.node('A1', '1. Arithmetic Terms/Symbols, Read/Write Numbers')
    graph.node('A2', '2. Count Flexibly, Sort Numbers, Overturn Results')
    graph.node('A3', '3. Add, Subtract, Multiply, Divide, Potentiate')
    graph.node('A4', '4. Compare/Transform Terms, Solve Equations, Apply Laws/Rules')
    
    # Sub-nodes for 'Exploring and Arguing'
    graph.node('B1', '1. Explore Numerical/Surgical Relationships, Arithmetic Patterns')
    graph.node('B2', '2. Explain, Check, Justify Statements, Assumptions, Results')
    graph.node('B3', '3. Use Tools for Researching Arithmetic Patterns')
    
    # Sub-nodes for 'Mathematize and Present'
    graph.node('C1', '1. Present, Describe, Exchange, Understand Calculation Paths')
    graph.node('C2', '2. Illustrate, Describe, Generalize Numbers, Sequences of Numbers, Terms')

    # Creating edges to denote dependencies and flow
    graph.edges([('1', 'A'), ('1', 'B'), ('1', 'C')])
    graph.edges([('A', 'A1'), ('A', 'A2'), ('A', 'A3'), ('A', 'A4')])
    graph.edges([('B', 'B1'), ('B', 'B2'), ('B', 'B3')])
    graph.edges([('C', 'C1'), ('C', 'C2')])
    
    return graph

# Create the graph
education_graph = create_education_graph()

# Display the graph in Streamlit

st.graphviz_chart(education_graph, use_container_width=True)


# Create a new directed graph
G = nx.DiGraph()

# Add nodes
nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
G.add_nodes_from(nodes)

# Add edges based on dependencies
edges = [
    ('a', 'b'), 
    ('b', 'c'), 
    ('b', 'e'), 
    ('c', 'e'),
    ('e', 'f'), 
    ('f', 'g'), 
    ('g', 'h'), 
    ('e', 'h'),
    ('h', 'i'), 
    ('i', 'j'), 
    ('j', 'k'), 
    ('k', 'l'),
    # Assuming 'd' might be a foundational concept for understanding ratios in later subjects
    ('d', 'e'), ('d', 'f'), ('d', 'g'), ('d', 'h')
]

G.add_edges_from(edges)

# Optional: Position nodes using the spring layout
pos = nx.spring_layout(G)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=16, arrowstyle='->', arrowsize=20)
plt.title('Knowledge Graph of Mathematical Concepts', size=20)


st.pyplot(plt)

