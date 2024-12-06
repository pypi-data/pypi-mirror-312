def set_boundary(T_in=300, P_in=101325, m_in=0.1, P_out=101325, T_out=300, gas_type="N2"):
    """
    A function to set the inputs for the boundary conditions (or at least the default)
    Can take custom values for T_in, P_in, etc.
    Parameters
    ----------
    T_in: initial field and inlet temperature in Kelvin
    P_in: initial field and inlet pressure in Pa
    m_in: mass flow rate for initial field and inlet kg/s
    P_out: outlet pressure of first cell in Pa
    T_out: outlet temperature of first cell in Kelvin
    gas_type: "N2" or "Air"
    Returns
    -------
    """
    return {
        'T_in': T_in,
        'P_in': P_in,
        'm_in': m_in,
        'P_out': P_out,
        'T_out': T_out,
        'gas_type': gas_type
    }