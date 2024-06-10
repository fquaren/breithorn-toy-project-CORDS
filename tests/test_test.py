import numpy as np
import pandas as pd
import pytest

# Import functions from the mass balance model module
from melt import synthetic_P, synthetic_T, lapse, melt, accumulate, main


def test_synthetic_P():
    assert synthetic_P(0) == 8e-3
    assert synthetic_P(100) == 8e-3


def test_synthetic_T():
    t = np.array([0, 91, 182, 273, 364])
    expected_T = np.array([-13, -3, 7, -3, -13])
    np.testing.assert_array_almost_equal([synthetic_T(time) for time in t], expected_T, decimal=1)


def test_lapse():
    assert lapse(10, 1000, -0.0065) == pytest.approx(3.5, 0.1)
    assert lapse(-5, 2000, -0.0065) == pytest.approx(-18, 0.1)


def test_melt():
    assert melt(10, 1.0) == 10
    assert melt(-5, 1.0) == 0
    assert melt(20, 0.5) == 10
    assert melt(0, 2.0) == 0


def test_accumulate():
    assert accumulate(-5, 10, 0) == 10
    assert accumulate(5, 10, 0) == 0
    assert accumulate(0, 10, 0) == 10
    assert accumulate(-1, 5, -1) == 5
    assert accumulate(1, 5, -1) == 0


def test_main(monkeypatch):
    # Create a mock dataset
    data = {
        "111": [1, 2, 3, 4, 5],
        "year": [2000, 2000, 2000, 2000, 2000],
        "day": [0, 91, 182, 273, 364],
        "hour": [0, 0, 0, 0, 0],
        "rel. humidity": [0, 0, 0, 0, 0],
        "air temp.": [0, 0, 0, 0, 0],
        "perciptation [mm / 30min]": [0, 0, 0, 0, 0],
        "batt. voltage": [0, 0, 0, 0, 0],
        "internal temp": [0, 0, 0, 0, 0]
    }
    df = pd.DataFrame(data)
    
    # Mock the read_csv function to return the mock dataset
    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: df)
    
    t, T, M, A, P = main()
    expected_t = np.array([0, 91, 182, 273, 364])
    expected_T = np.array([-13, -3, 7, -3, -13])
    expected_P = np.array([8e-3, 8e-3, 8e-3, 8e-3, 8e-3])
    expected_M = np.array([-13, -3, 7, -3, -13])
    expected_A = np.array([8e-3, 8e-3, 0, 8e-3, 8e-3])
    
    np.testing.assert_array_almost_equal(t, expected_t)
    np.testing.assert_array_almost_equal(T, expected_T)
    np.testing.assert_array_almost_equal(P, expected_P)
    np.testing.assert_array_almost_equal(M, expected_M)
    np.testing.assert_array_almost_equal(A, expected_A)


if __name__ == '__main__':
    pytest.main()
