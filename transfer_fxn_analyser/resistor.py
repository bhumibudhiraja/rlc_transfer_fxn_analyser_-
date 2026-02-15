# resistor.py

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QInputDialog
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import QRectF, Qt
from terminal import Terminal


class Resistor(QGraphicsItem):
    counter = 1

    def __init__(self, x, y):
        super().__init__()

        self.setPos(x, y)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.value = 1000
        self.name = f"R{Resistor.counter}"
        Resistor.counter += 1

        self.terminal1 = Terminal(self, 0, 10)
        self.terminal2 = Terminal(self, 80, 10)

        self.setTransformOriginPoint(self.boundingRect().center())

        self.text = QGraphicsTextItem(f"{self.name}\n{self.value} Ω", self)
        self.text.setPos(20, -25)

    def boundingRect(self):
        return QRectF(0, 0, 80, 20)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.GlobalColor.black))
        if self.isSelected():
            painter.setPen(QPen(Qt.GlobalColor.red, 2))

        painter.drawRect(10, 5, 60, 10)
        painter.drawLine(0, 10, 10, 10)
        painter.drawLine(70, 10, 80, 10)

    def mouseDoubleClickEvent(self, event):
        value, ok = QInputDialog.getDouble(
            None, "Edit Resistor", "Resistance (Ohms):",
            self.value, 0.0001, 1e12, 4
        )
        if ok:
            self.value = value
            self.text.setPlainText(f"{self.name}\n{self.value} Ω")

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for t in [self.terminal1, self.terminal2]:
                for wire in t.wires:
                    wire.update_position()
        return super().itemChange(change, value)