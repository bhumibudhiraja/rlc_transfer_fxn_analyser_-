# ground.py

from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import QRectF, Qt

from terminal import Terminal


class Ground(QGraphicsItem):

    def __init__(self, x, y):
        super().__init__()

        self.setPos(x, y)

        # Allow move + select + rotation
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        # Single terminal
        self.terminal = Terminal(self, 0, 0)

        # Mark this net as ground (IMPORTANT FIX)
        self.terminal.net.is_ground = True

        # Rotation center
        self.setTransformOriginPoint(self.boundingRect().center())

    # --------------------------------------

    def boundingRect(self):
        return QRectF(-10, 0, 20, 20)

    # --------------------------------------

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.GlobalColor.black))

        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 2))

        painter.drawLine(0, 0, 0, 6)
        painter.drawLine(-8, 6, 8, 6)
        painter.drawLine(-5, 9, 5, 9)
        painter.drawLine(-2, 12, 2, 12)

    # --------------------------------------

    def itemChange(self, change, value):

        # Update wires when moved
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for wire in self.terminal.wires:
                wire.update_position()

        return super().itemChange(change, value)