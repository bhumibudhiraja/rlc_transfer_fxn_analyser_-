from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter

from terminal import Terminal


class VoutMarker(QGraphicsItem):

    def __init__(self, x, y):
        super().__init__()
        self.setPos(x, y)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.terminal = Terminal(self, 0, 0)

    def boundingRect(self):
        return QRectF(-20, -20, 40, 40)

    def paint(self, painter, option, widget):
        painter.drawText(-15, 5, "VOUT")