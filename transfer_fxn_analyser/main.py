# main.py

import sys
from sympy import symbols, Matrix, simplify

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QGraphicsView,
    QGraphicsScene, QGraphicsTextItem
)
from PyQt6.QtCore import Qt

from resistor import Resistor
from capacitor import Capacitor
from inductor import Inductor
from ground import Ground
from wire import Wire
from terminal import Terminal


# ==========================================
# SCHEMATIC SCENE
# ==========================================

class SchematicScene(QGraphicsScene):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    # --------------------------------------
    # MOUSE CLICK
    # --------------------------------------

    def mousePressEvent(self, event):

        item = self.itemAt(event.scenePos(), self.views()[0].transform())

        if isinstance(item, Terminal):

            # ---------- VIN selection ----------
            if self.main_window.selecting_vin:
                self.main_window.vin_net = item.net

                if self.main_window.vin_label:
                    self.removeItem(self.main_window.vin_label)

                label = QGraphicsTextItem("VIN")
                label.setDefaultTextColor(Qt.GlobalColor.blue)
                label.setPos(item.scenePos())
                self.addItem(label)

                self.main_window.vin_label = label

                print("VIN selected")
                self.main_window.selecting_vin = False
                return

            # ---------- VOUT selection ----------
            if self.main_window.selecting_vout:
                self.main_window.vout_net = item.net

                if self.main_window.vout_label:
                    self.removeItem(self.main_window.vout_label)

                label = QGraphicsTextItem("VOUT")
                label.setDefaultTextColor(Qt.GlobalColor.darkGreen)
                label.setPos(item.scenePos())
                self.addItem(label)

                self.main_window.vout_label = label

                print("VOUT selected")
                self.main_window.selecting_vout = False
                return

            # ---------- Wiring ----------
            if self.main_window.selected_terminal is None:
                self.main_window.selected_terminal = item
            else:
                item.connect_to(self.main_window.selected_terminal)

                wire = Wire(item, self.main_window.selected_terminal)
                wire.setZValue(1)
                self.addItem(wire)

                self.main_window.selected_terminal = None

        else:
            self.main_window.selected_terminal = None

        super().mousePressEvent(event)

    # --------------------------------------
    # KEYBOARD
    # --------------------------------------

    def keyPressEvent(self, event):

        # Rotate
        if event.key() == Qt.Key.Key_R:
            for item in self.selectedItems():

                item.setRotation(item.rotation() + 90)

                if hasattr(item, "terminal1"):
                    for t in [item.terminal1, item.terminal2]:
                        for wire in t.wires:
                            wire.update_position()

                if hasattr(item, "terminal"):
                    for wire in item.terminal.wires:
                        wire.update_position()

        # Delete
        if event.key() == Qt.Key.Key_Delete:
            for item in self.selectedItems():

                if hasattr(item, "terminal1"):
                    for t in [item.terminal1, item.terminal2]:
                        for wire in list(t.wires):
                            self.removeItem(wire)

                if hasattr(item, "terminal"):
                    for wire in list(item.terminal.wires):
                        self.removeItem(wire)

                self.removeItem(item)

        super().keyPressEvent(event)


# ==========================================
# MAIN WINDOW
# ==========================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RLC Solver")
        self.setGeometry(100, 100, 1200, 700)

        self.selected_terminal = None
        self.selecting_vin = False
        self.selecting_vout = False
        self.vin_net = None
        self.vout_net = None

        self.vin_label = None
        self.vout_label = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Buttons
        self.btn_res = QPushButton("Add Resistor")
        self.btn_cap = QPushButton("Add Capacitor")
        self.btn_ind = QPushButton("Add Inductor")
        self.btn_gnd = QPushButton("Add Ground")
        self.btn_vin = QPushButton("Select VIN")
        self.btn_vout = QPushButton("Select VOUT")
        self.btn_analyze = QPushButton("Analyze Circuit")

        layout.addWidget(self.btn_res)
        layout.addWidget(self.btn_cap)
        layout.addWidget(self.btn_ind)
        layout.addWidget(self.btn_gnd)
        layout.addWidget(self.btn_vin)
        layout.addWidget(self.btn_vout)
        layout.addWidget(self.btn_analyze)

        self.scene = SchematicScene(self)
        self.view = QGraphicsView(self.scene)

        self.view.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.view.setFocus()

        layout.addWidget(self.view)

        # Connections
        self.btn_res.clicked.connect(lambda: self.scene.addItem(Resistor(100, 100)))
        self.btn_cap.clicked.connect(lambda: self.scene.addItem(Capacitor(200, 150)))
        self.btn_ind.clicked.connect(lambda: self.scene.addItem(Inductor(300, 200)))
        self.btn_gnd.clicked.connect(lambda: self.scene.addItem(Ground(400, 300)))

        self.btn_vin.clicked.connect(self.enable_vin_selection)
        self.btn_vout.clicked.connect(self.enable_vout_selection)
        self.btn_analyze.clicked.connect(self.analyze_circuit)

    # --------------------------------------

    def enable_vin_selection(self):
        print("Click terminal to set VIN")
        self.selecting_vin = True

    def enable_vout_selection(self):
        print("Click terminal to set VOUT")
        self.selecting_vout = True

    # --------------------------------------
    # SOLVER
    # --------------------------------------

    def analyze_circuit(self):

        if self.vin_net is None or self.vout_net is None:
            print("Select VIN and VOUT first!")
            return

        s = symbols('s')

        components = []
        nets = set()

        for item in self.scene.items():

            if hasattr(item, "terminal1"):
                components.append(item)
                nets.add(item.terminal1.net)
                nets.add(item.terminal2.net)

            if hasattr(item, "terminal"):
                nets.add(item.terminal.net)

        nets = list(nets)

        # Find GND
        gnd = None
        for net in nets:
            if hasattr(net, "is_ground") and net.is_ground:
                gnd = net

        if gnd is None:
            print("No GND found")
            return

        # Node mapping
        node_map = {}
        idx = 0
        for net in nets:
            if net is not gnd:
                node_map[net] = idx
                idx += 1

        N = len(node_map)
        M = 1

        A = Matrix.zeros(N + M, N + M)
        z = Matrix.zeros(N + M, 1)

        # Stamp passives
        for comp in components:

            n1 = comp.terminal1.net
            n2 = comp.terminal2.net

            if comp.__class__.__name__ == "Resistor":
                y = 1 / comp.value
            elif comp.__class__.__name__ == "Capacitor":
                y = s * comp.value
            elif comp.__class__.__name__ == "Inductor":
                y = 1 / (s * comp.value)
            else:
                continue

            if n1 is not gnd:
                i = node_map[n1]
                A[i, i] += y

            if n2 is not gnd:
                j = node_map[n2]
                A[j, j] += y

            if n1 is not gnd and n2 is not gnd:
                i = node_map[n1]
                j = node_map[n2]
                A[i, j] -= y
                A[j, i] -= y

        # Stamp VIN source
        k = N

        if self.vin_net is not gnd:
            i = node_map[self.vin_net]
            A[i, k] += 1
            A[k, i] += 1

        z[k] = 1

        solution = A.LUsolve(z)

        vout_index = node_map[self.vout_net]
        vout = simplify(solution[vout_index])

        print("\nTransfer Function H(s) = Vout/Vin:")
        print(vout)


# ==========================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())