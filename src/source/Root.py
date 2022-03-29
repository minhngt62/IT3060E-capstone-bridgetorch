from src.source.Node import Node


class Root(Node):
    def __init__(self, problem):
        Node.__init__(self, problem=problem, state=problem.init_state, parent=None, action=None)

