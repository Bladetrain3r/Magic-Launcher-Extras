import unittest
from src.topological_mapping.som_mapper import initialize_cpu_map_model, update_cpu_map
from src.topological_mapping.kuramoto_som import calculate_cluster_coherence

class TestSOMMapper(unittest.TestCase):

    def setUp(self):
        self.grid_dims = (10, 10)
        self.feature_dim = 5
        self.cpu_map = initialize_cpu_map_model(self.grid_dims, self.feature_dim)

    def test_initialize_cpu_map_model(self):
        self.assertEqual(len(self.cpu_map), self.grid_dims[0])
        self.assertEqual(len(self.cpu_map[0]), self.grid_dims[1])
        self.assertEqual(len(self.cpu_map[0][0]), self.feature_dim)

    def test_update_cpu_map(self):
        process_features = [0.5] * self.feature_dim
        bmu_index = update_cpu_map(process_features)
        self.assertIsInstance(bmu_index, tuple)
        self.assertEqual(len(bmu_index), 2)

    def test_calculate_cluster_coherence(self):
        bmu_index = (5, 5)
        coherence = calculate_cluster_coherence(bmu_index)
        self.assertIsInstance(coherence, float)
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)

if __name__ == '__main__':
    unittest.main()