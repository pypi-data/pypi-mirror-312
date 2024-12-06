from gocadgo.network import Network
from gocadgo.cell import Cell, StartCell
from helper import set_boundary
from plotter import show_fields
def main():
    # set boundary conditions:
    my_inlet = set_boundary(T_in=300,
                 P_in=101325,
                 m_in=0.1,
                 P_out=101325,
                 T_out=300,
                 gas_type="N2"
                 )

    # create mesh and run network:
    sky_train = Network(8, 8, 20, my_inlet)

    # display fields of interest:
    show_fields(sky_train, 'q')

if __name__ == "__main__":
    main()
