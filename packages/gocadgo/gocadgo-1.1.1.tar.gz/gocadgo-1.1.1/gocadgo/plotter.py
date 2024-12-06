import numpy as np
from cell import Cell, StartCell
def show_fields(network, field = 'T_in'):
    # Method 1: Use np.vectorize to access the T_in attribute of each cell
    vT_in = np.vectorize(lambda cell: cell.field)
    T_in_values = vT_in(network)
    print(T_in_values)