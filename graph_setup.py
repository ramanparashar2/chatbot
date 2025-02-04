# --------------------------
# graph_setup.py
# --------------------------
from langgraph.graph import END, StateGraph, START

from models import GraphState

class WorkflowBuilder:
    def __init__(self):
        self.workflow = StateGraph(GraphState)

    def add_node(self, name, func):
        self.workflow.add_node(name, func)

    def add_conditional_edge(self, start_node, condition, path_map):
        self.workflow.add_conditional_edges(start_node, condition, path_map)

    def add_edge(self, source, destination):
        self.workflow.add_edge(source, destination)

    def compile(self):
        return self.workflow.compile()