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



if __name__ == '__main__':
    pytest.main()
