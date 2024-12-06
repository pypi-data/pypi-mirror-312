import unittest
import os
from Turing_Pattern_Simulator.main import simulator

class TestSimulator(unittest.TestCase):

    def test_simulator_creates_png(self):
        """Test if simulator creates a PNG file correctly."""
        output_file = "test_simulation_output"
        simulator(
            grid_size=50,
            time_steps=100,
            F=0.04,
            k=0.06,
            D_u=0.16,
            D_v=0.08,
            output_type="png",
            filename=output_file
        )
        self.assertTrue(os.path.exists(f"{output_file}.png"))

        os.remove(f"{output_file}.png")

    def test_simulator_with_noise(self):
        """Test simulator with noise enabled."""
        output_file = "test_simulation_with_noise"
        simulator(
            grid_size=50,
            time_steps=100,
            F=0.04,
            k=0.06,
            D_u=0.16,
            D_v=0.08,
            add_noise=True,
            noise_U_to_V=0.05,
            noise_V_to_U=0.05,
            output_type="png",
            filename=output_file
        )
        self.assertTrue(os.path.exists(f"{output_file}.png"))

        # Cleanup
        os.remove(f"{output_file}.png")

    def test_simulator_with_gif(self):
        """Test simulator with gif."""
        output_file = "test_simulation_with_gif"
        simulator(
            grid_size=50,
            time_steps=100,
            F=0.04,
            k=0.06,
            D_u=0.16,
            D_v=0.08,
            add_noise=True,
            noise_U_to_V=0.05,
            noise_V_to_U=0.05,
            output_type="gif",
            filename=output_file
        )
        self.assertTrue(os.path.exists(f"{output_file}.gif"))

        # Cleanup
        os.remove(f"{output_file}.gif")


if __name__ == '__main__':
    unittest.main()
