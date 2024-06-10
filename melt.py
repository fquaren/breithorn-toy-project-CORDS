"""Simple glacier mass balance model."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


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
def accumulate(T, P, T_threshold):
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
    #weather_data = "./data/workshop-reproducible-research/own"
    #columns = ["111", "year", "day", "hour", "rel. humidity", "air temp.", "perciptation [mm / 30min]", "batt. voltage", "internal temp"]
    #ds = pd.read_csv(weather_data, names=columns)
    #t = ds["day"].to_numpy()
    
    t = np.arange(0, 365, 1.24)
    
    # Model parameters
    melt_factor = 0.005  # Melt factor
    T_threshold = 4.0  # Threshold temperature
    lapse_rate = -0.6/100  # Temperature lapse rate
    x = np.arange(0, 5000, 500) 
    # Init
    M = np.zeros(len(t))
    Ts = np.zeros(len(t))
    A = np.zeros(len(t))
    Ps = np.zeros(len(t))
    z_station = 1500
    z_point = [z_station]
    hist_point_norm_glacier_net_balance = []
    hist_point_net_balance = []
    hist_norm_glacier_net_balance = []
    hist_net_balance = []
    # Compute
    zs = [i/5+1400-z_station for i in x]
    for i, dt in enumerate(t):
        Ts[i] = synthetic_T(dt)
        Ps[i] = synthetic_P(dt)
        # Point balance
        point_norm_glacier_net_balance, point_net_balance = glacier_net_balance_fn(z_point, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
        hist_point_norm_glacier_net_balance.append(point_norm_glacier_net_balance)
        hist_point_net_balance.append(point_net_balance)
        # Glacier wide balance
        norm_glacier_net_balance, net_balance = glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
        hist_norm_glacier_net_balance.append(norm_glacier_net_balance)
        hist_net_balance.append(net_balance)
    return t, x, Ts, hist_point_norm_glacier_net_balance, hist_point_net_balance, hist_norm_glacier_net_balance, hist_net_balance


if __name__ == '__main__':
    t, x, Ts, hist_point_norm_glacier_net_balance, hist_point_net_balance, hist_norm_glacier_net_balance, hist_net_balance = main()

    # Plotting
    fig = plt.figure()
    plt.plot(t, Ts)
    plt.xlabel("Days")
    plt.ylabel("Temperature")
    plt.show()

    fig = plt.figure()
    plt.plot(t, hist_point_net_balance)
    plt.xlabel("Days")
    plt.ylabel("Point net balance (station)")
    plt.show()

    fig = plt.figure()
    color = iter(cm.rainbow(range(0, len(hist_net_balance), 10)))
    for e in range(0, len(hist_net_balance), 10):
        c = next(color)
        plt.scatter(x, hist_net_balance[e], c=c)
        plt.xlabel("Extent [m]")
        plt.ylabel("Net balance (glacier)")
    plt.show()
