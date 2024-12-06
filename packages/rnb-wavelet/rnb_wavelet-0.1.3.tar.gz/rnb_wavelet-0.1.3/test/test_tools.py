import unittest
import numpy as np
from rnb.utils.tools import compute_spectrum

class TestTools(unittest.TestCase):
    def test_some_function(self):
        # Test inputs
        fs = 1000  # Sampling frequency in Hz
        data_epocs = np.random.rand(2, 1024)  # Ensure the input is 2D
        
        # Call the function
        freq, F = compute_spectrum(data_epocs, fs)
        
        # Expected outputs
        expected_freq = fs / 2 * np.linspace(0, 1, 1024 // 2 + 1)[1:]  # Skip null frequency
        expected_F_shape = (1, len(expected_freq))  # 1 epoch, matching freq length
        
        # Assertions
        np.testing.assert_array_almost_equal(freq, expected_freq, decimal=5)  # Compare frequency arrays
        self.assertEqual(F.shape, expected_F_shape)  # Compare shape of power spectrum

if __name__ == "__main__":
    unittest.main()
