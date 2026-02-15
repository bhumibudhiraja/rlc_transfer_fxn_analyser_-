# circuit_graph.py

class CircuitGraph:
    """
    Pure data model of the circuit.
    No GUI code here.
    No PyQt imports.
    """

    def __init__(self):
        self.components = []
        self.nets = []

    # -----------------------------
    # Component Handling
    # -----------------------------

    def add_component(self, component):
        self.components.append(component)

    # -----------------------------
    # Net Handling
    # -----------------------------

    def add_net(self, net):
        if net not in self.nets:
            self.nets.append(net)

    def merge_nets(self, net1, net2):
        """
        Merge net2 into net1
        """
        if net1 is net2:
            return

        for terminal in net2.terminals:
            terminal.net = net1
            net1.terminals.add(terminal)

        if net2 in self.nets:
            self.nets.remove(net2)

    # -----------------------------
    # Utility
    # -----------------------------

    def get_net_by_name(self, name):
        for net in self.nets:
            if net.name == name:
                return net
        return None

    def build_node_index_map(self):
        """
        Builds node index mapping excluding GND.
        Returns dictionary: net -> index
        """

        node_map = {}
        index = 0

        for net in self.nets:
            if net.name == "GND":
                continue

            node_map[net] = index
            index += 1

        return node_map

    # -----------------------------
    # Debug
    # -----------------------------

    def print_debug(self):
        print("=== Circuit Debug ===")
        print("Components:", len(self.components))
        print("Nets:", len(self.nets))

        for net in self.nets:
            print(f"Net: {net.name}, Terminals: {len(net.terminals)}")
