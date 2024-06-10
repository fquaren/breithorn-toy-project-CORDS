import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../src/')

import numpy as np
import pytest
from melt import melt, accumulate, lapse, net_balance_fn, glacier_net_balance_fn

def test_net_balance_fn():
    dt = 1.0  # time step
    Ts = np.array([-5, 0, 5, -3, 2])
    Ps = np.array([0.01, 0.02, 0.03, 0.04, 0.05])
    melt_factor = 1.0
    T_threshold = 0
    
    expected_balance = sum([-melt(T, melt_factor) + accumulate(T, P, T_threshold) for T, P in zip(Ts, Ps)]) * dt
    
    result = net_balance_fn(dt, Ts, Ps, melt_factor, T_threshold)
    assert np.isclose(result, expected_balance)

def test_glacier_net_balance_fn():
    zs = np.array([0, 500, 1000])
    dt = 1.0
    Ts = np.array([-5, 0, 5, -3, 2])
    Ps = np.array([0.01, 0.02, 0.03, 0.04, 0.05])
    melt_factor = 1.0
    T_threshold = 0
    lapse_rate = -0.0065
    
    glacier_net_balance, net_balance = glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
    
    # Calculate expected glacier net balance
    expected_net_balances = []
    for z in zs:
        lapsed_Ts = [lapse(T, z, lapse_rate) for T in Ts]
        expected_net_balance = net_balance_fn(dt, lapsed_Ts, Ps, melt_factor, T_threshold)
        expected_net_balances.append(expected_net_balance)
        
    expected_glacier_net_balance = sum(expected_net_balances) / len(zs)
    
    assert np.isclose(glacier_net_balance, expected_glacier_net_balance)
    assert np.allclose(net_balance, expected_net_balances)

if __name__ == "__main__":
    pytest.main()