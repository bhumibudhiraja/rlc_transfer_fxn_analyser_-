# inductor.py

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QInputDialog
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import QRectF, Qt
from terminal import Terminal


class Inductor(QGraphicsItem):
    counter = 1

    def __init__(self, x, y):
        super().__init__()

        self.setPos(x, y)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.value = 1e-3
        self.name = f"L{Inductor.counter}"
        Inductor.counter += 1

        self.terminal1 = Terminal(self, 0, 20)
        self.terminal2 = Terminal(self, 80, 20)

        self.setTransformOriginPoint(self.boundingRect().center())

        self.text = QGraphicsTextItem(f"{self.name}\n{self.value} H", self)
        self.text.setPos(20, -25)

    def boundingRect(self):
        return QRectF(0, 0, 80, 40)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.GlobalColor.black))
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 2))

        painter.drawLine(0, 20, 10, 20)
        painter.drawLine(70, 20, 80, 20)
        painter.drawEllipse(10, 10, 15, 20)
        painter.drawEllipse(25, 10, 15, 20)
        painter.drawEllipse(40, 10, 15, 20)
        painter.drawEllipse(55, 10, 15, 20)

    def mouseDoubleClickEvent(self, event):
        value, ok = QInputDialog.getDouble(
            None, "Edit Inductor", "Inductance (H):",
            self.value, 1e-9, 1e3, 9
        )
        if ok:
            self.value = value
            self.text.setPlainText(f"{self.name}\n{self.value} H")

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for t in [self.terminal1, self.terminal2]:
                for wire in t.wires:
                    wire.update_position()
        return super().itemChange(change, value)