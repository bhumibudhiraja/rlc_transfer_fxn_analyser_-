# wire.py

from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt


class Wire(QGraphicsLineItem):
    def __init__(self, terminal1, terminal2):
        super().__init__()

        self.terminal1 = terminal1
        self.terminal2 = terminal2

        self.setPen(QPen(Qt.GlobalColor.blue, 2))

        # Register wire in terminals
        if not hasattr(terminal1, "wires"):
            terminal1.wires = []
        if not hasattr(terminal2, "wires"):
            terminal2.wires = []

        terminal1.wires.append(self)
        terminal2.wires.append(self)

        self.update_position()

    def update_position(self):
        p1 = self.terminal1.scenePos()
        p2 = self.terminal2.scenePos()

        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())