import numpy as np
from cell import Cell, StartCell
from helper import set_boundary
class Network:
    def __init__(self, height:int, width:int, length:int, boundary: dict = None):
        """
        Create a network object repressenting a heat exchanger.
        Parameters
        ----------
        height: by number of cells
        width: by number of cells
        length: by number of cells
        config :
        """

        # set boundary conditions to default if user hasn't specified them:
        if boundary is None:
            boundary = set_boundary()
        print(boundary)
        # the first row of cells should always be start cells:
        start_grid_size = (1, width, length)
        init_startCell = StartCell(**boundary) # boundary condition stored as dict
        start_network = np.full(start_grid_size, init_startCell, dtype=object)

        # now normal cells:
        grid_size = (height-1, width, length)
        init_Cell = StartCell(**boundary) # boundary condition stored as dict
        network = np.full(grid_size, init_Cell, dtype=object)

        # Combine the two networks (start_network + network)
        self.network = np.concatenate((start_network, network), axis=0)
        print(self.network.shape)

        print(self.network)

        # use Numpy ops over vectorisation:

        # Access a cell:
        print(f"Cell at (0, 0, 0): {self.network[0, 0, 0].T_in}")
        print(f"Cell at (10, 4, 5): {self.network[6, 4, 5].T_in}")

        # Modify a cell:
        self.network[0, 0, 0].T_in = 8.0
        self.network[0, 0, 0]._cp = 2.0

        print(f"Modified Cell at (0, 0, 0): {self.network[0, 0, 0]}")

