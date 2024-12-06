import unittest
import os
from Turing_Pattern_Simulator.main import sweeper_1d, sweeper_2d

class TestSweeper2D(unittest.TestCase):

    def test_sweeper_2d(self):
        """Test if sweeper_2d generates correct number of PNG files when matrix output is disabled."""
        output_dir = "test_sweeper_2d_results"
        param1_range = (0.01, 0.03, 0.02)
        param2_range = (0.06, 0.08, 0.02)

        # Calculate expected number of files
        param1_values = int((param1_range[1] - param1_range[0]) / param1_range[2]) + 1
        param2_values = int((param2_range[1] - param2_range[0]) / param2_range[2]) + 1
        expected_file_count = param1_values * param2_values + 1

        # Run sweeper_2d without matrix output
        sweeper_2d(
            param1_name='F',
            param1_range=param1_range,
            param2_name='k',
            param2_range=param2_range,
            simulator_args={
                'grid_size': 50,
                'time_steps': 100,
                'D_u': 0.16,
                'D_v': 0.08,
                'frame_interval': 10,
                'fps': 5,
                'add_noise': False,
                'noise_U_to_V': 0.05,
                'noise_V_to_U': 0.05
            },
            output_dir=output_dir,
        )

        # Check if folder exists
        self.assertTrue(os.path.exists(output_dir))

        # Check the number of generated PNG files
        generated_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
        self.assertEqual(len(generated_files), expected_file_count)

        # Cleanup
        for f in generated_files:
            os.remove(os.path.join(output_dir, f))
        os.rmdir(output_dir)

    def test_sweeper_2d_with_matrix(self):
        """Test if sweeper_2d generates a matrix PNG file when matrix output is enabled."""
        output_dir = "test_sweeper_2d_results_with_matrix"
        param1_range = (0.01, 0.05, 0.02)
        param2_range = (0.06, 0.1, 0.02)

        # Run sweeper_2d with matrix output
        sweeper_2d(
            param1_name='F',
            param1_range=param1_range,
            param2_name='k',
            param2_range=param2_range,
            simulator_args={
                'grid_size': 50,
                'time_steps': 100,
                'D_u': 0.16,
                'D_v': 0.08,
                'frame_interval': 10,
                'fps': 5,
                'add_noise': False,
                'noise_U_to_V': 0.05,
                'noise_V_to_U': 0.05
            },
            output_dir=output_dir,
        )

        # Check if matrix PNG file is created
        matrix_file = os.path.join(output_dir, "F_k_matrix.png")
        self.assertTrue(os.path.exists(matrix_file))

        # Cleanup
        if os.path.exists(matrix_file):
            os.remove(matrix_file)
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, f))
            os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()
