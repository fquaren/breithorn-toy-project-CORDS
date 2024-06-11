import numpy as np


# Precipitation function
def synthetic_P(t):
    """Returns a constant precipitation rate of 8e-3."""
    return 8e-3


# Synthetic temperature
def synthetic_T(t):
    """
    Calculates the synthetic temperature using a combination of two cosine functions.

    The first cosine function has a period of 364 days (representing a year) and the second has a period of 1 day.

    Args:
        t: Time variable, typically in days.

    Returns:
        float: Synthetic temperature value.
    """
    return -10.0*np.cos(2*np.pi/364 * t) - 8.0*np.cos(2*np.pi* t) + 5.0


# Lapsed temperature 
def lapse(T, dz, lapse_rate):
    """Calculates the lapsed temperature.

    Args:
        T: Original temperature.
        dz: Elevation change.
        lapse_rate: Rate of temperature change with elevation.

    Returns:
        float: Lapsed temperature.
    """
    return lapse_rate * dz + T


# Melt function
def melt(T, m):
    """
    Calculates the melt rate.

    Args:
        T: Temperature.
        m: Melt factor.

    Returns:
        float: Melt rate if temperature is above or equal to 0, otherwise returns 0.
    """
    if T >= 0:
        return m * T
    else:
        return 0
    

# Accumulation rate
def accumulate(T, P, T_threshold):
    """
    Calculates the accumulation rate.

    Args:
        T: Temperature.
        P: Precipitation rate.
        T_threshold: Temperature threshold for accumulation.

    Returns:
        float: Precipitation rate if temperature is below or equal to the threshold, otherwise returns 0.
    """
    if T <= T_threshold:
        return P
    else:
        return 0


def net_balance_fn(dt, Ts, Ps, melt_factor, T_threshold):
    """
    Integrate the balance rate (this is at a point) over time for given temperature and precipitation arrays to get the "net balance".

    Args:
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.

    Returns:
        net balance (this is at a point)
    """
    assert len(Ts) == len(Ps)
    total = 0.0
    for T, P in zip(Ts, Ps):
        balance_rate = -melt(T, melt_factor) + accumulate(T, P, T_threshold)
        total += balance_rate * dt
    return total


def glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate):
    """
    Calculate:
    - the glacier net balance (integration of balance rate over time and space)
    - the net balance at each point (integration of balance rate over time)

    Args:
        zs: Array of elevations (with the weather station as datum)
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.
        lapse_rate: The lapse rate (temperature change per unit elevation change).

    Returns:
        the glacier net balance [m]
        net balance at all points [m]
    """
    glacier_net_balance = 0.0
    net_balance = np.zeros(len(zs))
    for i, z in enumerate(zs):
        TT = [lapse(T, z, lapse_rate) for T in Ts]
        net_balance[i] = net_balance_fn(dt, TT, Ps, melt_factor, T_threshold)
        glacier_net_balance += net_balance[i]
    return glacier_net_balance / len(zs), net_balance
    