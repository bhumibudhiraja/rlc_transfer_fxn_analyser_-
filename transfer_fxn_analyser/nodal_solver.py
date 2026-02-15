import sympy as sp


def solve_transfer_function(graph):
    """
    Compute symbolic transfer function H(s)
    using nodal analysis.
    """

    s = sp.symbols('s')

    nodes = sorted(graph.get_nodes())

    if 0 not in nodes:
        nodes.append(0)

    # Remove ground node
    active_nodes = [n for n in nodes if n != 0]

    if len(active_nodes) < 2:
        raise ValueError("Need at least two nodes")

    N = len(active_nodes)

    Y = sp.zeros(N)
    I = sp.zeros(N, 1)

    node_index = {node: i for i, node in enumerate(active_nodes)}

    # Build admittance matrix
    for comp_type, value, n1, n2 in graph.components:

        if comp_type == "R":
            Yval = 1 / value
        elif comp_type == "C":
            Yval = s * value
        elif comp_type == "L":
            Yval = 1 / (s * value)
        else:
            continue

        if n1 != 0:
            i = node_index[n1]
            Y[i, i] += Yval

        if n2 != 0:
            j = node_index[n2]
            Y[j, j] += Yval

        if n1 != 0 and n2 != 0:
            i = node_index[n1]
            j = node_index[n2]
            Y[i, j] -= Yval
            Y[j, i] -= Yval

    # Assume first node = Vin, last node = Vout
    Vin_node = active_nodes[0]
    Vout_node = active_nodes[-1]

    Vin_index = node_index[Vin_node]
    Vout_index = node_index[Vout_node]

    # Inject 1V test source
    I[Vin_index] = 1

    # 🔥 FAST solve (no full inverse)
    V = Y.LUsolve(I)

    H = sp.simplify(V[Vout_index])

    return H
