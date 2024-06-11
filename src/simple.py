import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

from melt import *
from utils import make_sha_filename


def main():
    # Model parameters
    melt_factor = 0.005  # Melt factor
    T_threshold = 4.0  # Threshold temperature
    lapse_rate = -0.6/100  # Temperature lapse rate
    # Init
    x = np.arange(0, 5000, 500)  # Glacier extent
    t = np.arange(0, 365, 1.24)
    M = np.zeros(len(t))
    Ts = np.zeros(len(t))
    A = np.zeros(len(t))
    Ps = np.zeros(len(t))
    z_station = 1500
    z_point = [z_station]
    Toffs = range(-4, 5)
    point_net_balance = np.zeros((len(t), 1))
    net_balance = np.zeros((len(t), len(x)))
    out = np.zeros(len(Toffs))
    # Compute
    zs = [i/5+1400-z_station for i in x]
    for i, dt in enumerate(t):
        Ts[i] = synthetic_T(dt)
        Ps[i] = synthetic_P(dt)
        # Point balance
        _, point_net_balance[i, :] = glacier_net_balance_fn(z_point, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
        # Glacier wide balance
        _, net_balance[i, :] = glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
    for k, Toff in enumerate(Toffs):
        for i, dt in enumerate(t):
            out[k], _ = glacier_net_balance_fn(zs, dt, Ts+Toff, Ps, melt_factor, T_threshold, lapse_rate)

    # Plotting
    fig = plt.figure()
    plt.plot(t, Ts)
    plt.xlabel("Days")
    plt.ylabel("Temperature")
    plt.savefig(make_sha_filename("Synthetic-T", ".png"))

    fig = plt.figure()
    plt.plot(t, point_net_balance)
    plt.xlabel("Days")
    plt.ylabel("Pet balance (station)")
    # plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    X, Y = np.meshgrid(x, t)
    ax.plot_surface(Y, X, net_balance)
    ax.set_xlabel("Time [day]")
    ax.set_ylabel("Extent [m]")
    ax.set_zlabel("Net balance (glacier-wide)")
    # plt.show()

    fig = plt.figure()
    plt.scatter(Toffs, out)
    plt.xlabel("T_off [C]")
    plt.ylabel("Total net balance (glacier-wide)")
    plt.grid()
    # plt.show()

    # 


if __name__ == '__main__':
    main()