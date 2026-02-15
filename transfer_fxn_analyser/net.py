# net.py

class Net:
    def __init__(self, name=None):
        self.name = name
        self.terminals = set()

    def add_terminal(self, terminal):
        self.terminals.add(terminal)
        terminal.net = self