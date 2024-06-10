"""Simple glacier mass balance model."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb


# Precipitation function
def synthetic_P(t):
    return 8e-3


# Synthetic temperature
def synthetic_T(t):    
    return -10.0*np.cos(2*np.pi/364 * t) - 8.0*np.cos(2*np.pi* t) + 5.0


# Lapsed temperature 
def lapse(T, dz, lapse_rate):
    return lapse_rate * dz + T


# Melt function
def melt(T, m):
    if T >= 0:
        return m * T
    else:
        return 0
    

# Accumulation rate
def accumlate(T, P, T_threshold):
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

def main():
    # Data
    weather_data = "./data/workshop-reproducible-research/own"
    columns = ["111", "year", "day", "hour", "rel. humidity", "air temp.", "perciptation [mm / 30min]", "batt. voltage", "internal temp"]
    ds = pd.read_csv(weather_data, names=columns)
    t = ds["day"].to_numpy()
    # Model parameters
    m = 1.0  # Melt factor
    T_threshold = 4.0  # Threshold temperature
    dz = 0.0
    # Compute melt
    M = np.zeros(len(t))
    T = np.zeros(len(t))
    A = np.zeros(len(t))
    P = np.zeros(len(t))
    for i, time in enumerate(t):
        T[i] = synthetic_T(time)
        P[i] = synthetic_P(time)
        M[i] = melt(m, T[i])
        A[i] = accumlate(T[i], P[i], T_threshold)
    return t, T, M, A, P


if __name__ == '__main__':
    t, T, M, A, P = main()
    
    # Plotting
    fig = plt.figure()
    plt.plot(t, M)
    plt.xlabel("Days")
    plt.ylabel("Melt")
    plt.show()

    fig = plt.figure()
    plt.plot(t, A)
    plt.xlabel("Days")
    plt.ylabel("Accumulation")
    plt.show()
