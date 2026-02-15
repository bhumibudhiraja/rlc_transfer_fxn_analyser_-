# terminal.py

from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt


class Net:
    def __init__(self):
        self.terminals = []
        self.is_ground = False  # Important


class Terminal(QGraphicsEllipseItem):

    def __init__(self, parent, x, y):
        super().__init__(-4, -4, 8, 8, parent)

        self.setBrush(QBrush(Qt.GlobalColor.red))
        self.setPos(x, y)

        self.net = Net()
        self.net.terminals.append(self)

        self.wires = []

    # -------------------------------------

    def connect_to(self, other_terminal):

        if self.net is other_terminal.net:
            return

        net1 = self.net
        net2 = other_terminal.net

        # Preserve ground flag
        if net1.is_ground or net2.is_ground:
            net1.is_ground = True
            net2.is_ground = True

        # Merge net2 into net1
        for terminal in net2.terminals:
            terminal.net = net1
            net1.terminals.append(terminal)

        net2.terminals.clear()