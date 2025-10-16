import unittest
from src.proprioception.data_collector import collect_process_metrics
from unittest.mock import patch
import time

class TestDataCollector(unittest.TestCase):

    @patch('src.proprioception.data_collector.psutil')
    def test_collect_process_metrics(self, mock_psutil):
        # Mock the psutil process and its CPU percent method
        mock_process = mock_psutil.Process.return_value
        mock_process.cpu_percent.return_value = 25.0
        mock_psutil.process_iter.return_value = [mock_process]

        # Call the function with a sampling rate
        sampling_rate_hz = 1  # 1 Hz
        metrics = collect_process_metrics(sampling_rate_hz)

        # Check if the metrics are collected correctly
        self.assertIsInstance(metrics, dict)
        self.assertIn('pid', metrics)
        self.assertIn('name', metrics)
        self.assertIn('cpu_percent', metrics)
        self.assertEqual(metrics['cpu_percent'], 25.0)

    @patch('src.proprioception.data_collector.psutil')
    def test_collect_process_metrics_multiple_samples(self, mock_psutil):
        # Mock the psutil process and its CPU percent method
        mock_process = mock_psutil.Process.return_value
        mock_process.cpu_percent.side_effect = [20.0, 30.0, 40.0]
        mock_psutil.process_iter.return_value = [mock_process]

        # Call the function multiple times to simulate sampling
        sampling_rate_hz = 1  # 1 Hz
        metrics_list = []
        for _ in range(3):
            metrics = collect_process_metrics(sampling_rate_hz)
            metrics_list.append(metrics)
            time.sleep(1)  # Simulate time delay for sampling

        # Check if the metrics are collected correctly
        self.assertEqual(len(metrics_list), 3)
        self.assertEqual(metrics_list[0]['cpu_percent'], 20.0)
        self.assertEqual(metrics_list[1]['cpu_percent'], 30.0)
        self.assertEqual(metrics_list[2]['cpu_percent'], 40.0)

if __name__ == '__main__':
    unittest.main()