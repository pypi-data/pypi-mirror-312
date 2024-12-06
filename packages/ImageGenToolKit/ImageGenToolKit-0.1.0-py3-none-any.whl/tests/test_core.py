import unittest
from unittest.mock import patch, MagicMock
import asyncio
from ImageGenToolKIT.core import AIImageGenerator


class TestAIImageGenerator(unittest.TestCase):
    def setUp(self):
        # Initialize the AIImageGenerator instance
        self.generator = AIImageGenerator()

    @patch('requests.get')  # Mock the requests.get method to avoid actual HTTP requests
    def test_get_random_proxy(self, mock_get):
        # Mock the response to return a list of proxies
        mock_get.return_value.text = "http://proxy1.com\nhttp://proxy2.com\nhttp://proxy3.com"
        
        proxies = self.generator.get_random_proxy()
        self.assertIsNotNone(proxies)
        self.assertIn('http', proxies)
        self.assertIn('https', proxies)
        self.assertTrue(proxies['http'].startswith("http://"))
        print(f"Tested get_random_proxy: {proxies}")

    @patch('requests.post')  # Mock the requests.post method to simulate a successful task creation
    def test_create_task(self, mock_post):
        task_response = {
            'status': 'QUEUED',
            'task_id': '12345'
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = task_response

        task_id = self.generator.generate_task_id()
        proxies = {"http": "http://proxy1.com", "https": "http://proxy1.com"}
        prompt = "A sample prompt"

        result = self.generator.create_task(task_id, proxies, prompt)
        self.assertEqual(result['status'], 'QUEUED')
        self.assertEqual(result['task_id'], '12345')
        print(f"Tested create_task: {result}")

    @patch('requests.get')  # Mock the requests.get method for checking task status
    def test_check_status_success(self, mock_get):
        status_response = {
            "status": "SUCCESS",
            "urls": ["https://example.com/image1.jpg"]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = status_response

        task_id = '12345'
        proxies = {"http": "http://proxy1.com", "https": "http://proxy1.com"}
        urls = self.generator.check_status(task_id, proxies)

        self.assertEqual(urls, ["https://example.com/image1.jpg"])
        print(f"Tested check_status: {urls}")

    @patch('requests.get')  # Mock the requests.get method for an invalid proxy
    def test_check_status_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        task_id = '12345'
        proxies = {"http": "http://proxy1.com", "https": "http://proxy1.com"}

        urls = self.generator.check_status(task_id, proxies)
        self.assertEqual(urls, [])
        print("Tested check_status with error: No URLs returned due to error")

    @patch('requests.get')  # Mock the requests.get method for no proxies returned
    def test_no_valid_proxy(self, mock_get):
        mock_get.return_value.text = ""
        
        proxies = self.generator.get_random_proxy()
        self.assertIsNone(proxies)
        print("Tested no valid proxy returned.")

    @patch('requests.get')  # Mock the requests.get method to simulate proxy failure
    def test_generate_image_failure(self, mock_get):
        # Simulating proxy failure scenario
        mock_get.return_value.text = "http://proxy1.com"
        task_response = {
            'status': 'FAILED'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = task_response

        prompt = "A test prompt"
        urls = self.generator.generate_image(prompt)

        self.assertEqual(urls, [])
        print("Tested image generation failure.")

    @patch('requests.get')  # Mocking the proxy for successful image generation
    def test_generate_image_success(self, mock_get):
        # Mock successful proxy and task creation
        mock_get.return_value.text = "http://proxy1.com"
        task_response = {
            'status': 'QUEUED',
            'task_id': '12345'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = task_response

        # Mock task completion status and image URLs
        status_response = {
            "status": "SUCCESS",
            "urls": ["https://example.com/image1.jpg"]
        }
        mock_get.return_value.json.return_value = status_response

        prompt = "A test prompt"
        urls = self.generator.generate_image(prompt)

        self.assertEqual(urls, ["https://example.com/image1.jpg"])
        print("Tested image generation success.")

if __name__ == "__main__":
    unittest.main()
