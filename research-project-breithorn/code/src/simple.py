import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from datetime import datetime
import os

from melt import *
from utils import make_sha_filename


def main():
    """Main function to run the glacier balance model and generate outputs."""
    
    # Model parameters
    melt_factor = 0.005  # Melt factor for the melt function
    T_threshold = 4.0  # Temperature threshold for accumulation
    lapse_rate = -0.6 / 100  # Lapse rate for temperature adjustment
    
    # Initialization of variables
    x = np.arange(0, 5000, 500)  # Spatial coordinate array
    t = np.arange(0, 365, 1.24)  # Time array in days
    M = np.zeros(len(t))  # Placeholder for melt values
    Ts = np.zeros(len(t))  # Placeholder for synthetic temperature values
    A = np.zeros(len(t))  # Placeholder for accumulation values
    Ps = np.zeros(len(t))  # Placeholder for synthetic precipitation values
    z_station = 1500  # Elevation of the weather station
    z_point = [z_station]  # List containing the station elevation
    Toffs = range(-4, 5)  # Temperature offsets for sensitivity analysis
    point_net_balance = np.zeros((len(t), 1))  # Net balance at a single point
    net_balance = np.zeros((len(t), len(x)))  # Glacier-wide net balance
    out = np.zeros(len(Toffs))  # Output array for sensitivity analysis
    
    # Compute synthetic temperatures and precipitation, and balance calculations
    zs = [i / 5 + 1400 - z_station for i in x]  # Elevation adjustments
    for i, dt in enumerate(t):
        Ts[i] = synthetic_T(dt)  # Calculate synthetic temperature
        Ps[i] = synthetic_P(dt)  # Calculate synthetic precipitation
        # Point net balance calculation
        _, point_net_balance[i, :] = glacier_net_balance_fn(
            z_point, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate
        )
        # Glacier-wide net balance calculation
        _, net_balance[i, :] = glacier_net_balance_fn(
            zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate
        )
    for k, Toff in enumerate(Toffs):
        for i, dt in enumerate(t):
            out[k], _ = glacier_net_balance_fn(
                zs, dt, Ts + Toff, Ps, melt_factor, T_threshold, lapse_rate
            )

    # Create output directory if it doesn't exist
    output_path = "output"
    os.makedirs(output_path, exist_ok=True)
    
    # Save synthetic temperature data to a CSV file
    np.savetxt(os.path.join(output_path, "Synthetic-T.csv"), Ts, delimiter=',')

    # Get the current date and time for file naming
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-")
    
    # Plotting synthetic temperature over time
    fig = plt.figure()
    plt.plot(t, Ts)
    plt.xlabel("Days")
    plt.ylabel("Temperature")
    plt.savefig(os.path.join(output_path, make_sha_filename(date + "Synthetic-T", ".png")))

    # Plotting point net balance over time
    fig = plt.figure()
    plt.plot(t, point_net_balance)
    plt.xlabel("Days")
    plt.ylabel("Net balance (station)")
    # plt.show()  # Uncomment to display the plot

    # 3D plot of glacier-wide net balance
    ax = plt.figure().add_subplot(projection='3d')
    X, Y = np.meshgrid(x, t)
    ax.plot_surface(Y, X, net_balance)
    ax.set_xlabel("Time [day]")
    ax.set_ylabel("Extent [m]")
    ax.set_zlabel("Net balance (glacier-wide)")
    # plt.show()  # Uncomment to display the plot

    # Scatter plot of total net balance with temperature offsets
    fig = plt.figure()
    plt.scatter(Toffs, out)
    plt.xlabel("T_off [C]")
    plt.ylabel("Total net balance (glacier-wide)")
    plt.grid()
    # plt.show()  # Uncomment to display the plot


if __name__ == '__main__':
    main()
