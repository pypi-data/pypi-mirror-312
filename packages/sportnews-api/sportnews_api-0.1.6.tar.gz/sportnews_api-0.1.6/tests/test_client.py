import unittest
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add project root to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews.client import SportNewsAPI
from sportnews.exceptions import SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = SportNewsAPI(
            api_key='sk_startup_6c1d8a80-4de6-4349-a479-f5be444ca6b9'
        )

    def validate_article(self, article: dict) -> None:
        """Validate the structure and content of a news article."""
        required_fields = ['title', 'description', 'published', 'sport', 'language']
        for field in required_fields:
            self.assertIn(field, article, f"Field {field} is missing")

        self.assertIsInstance(article['title'], str)
        self.assertIsInstance(article['description'], str)
        
        self.assertGreaterEqual(len(article['title']), 3)
        self.assertGreaterEqual(len(article['description']), 10)
        self.assertLessEqual(len(article['title']), 500)
        self.assertLessEqual(len(article['description']), 500)

        self.assertFalse(any(char in article['title'] for char in ['\n', '\r', '\t']))
        self.assertFalse(any(char in article['description'] for char in ['\n', '\r', '\t']))

        if article['sport']:
            self.assertIn(article['sport'], self.api.VALID_SPORTS)
        if article['language']:
            self.assertIn(article['language'], self.api.VALID_LANGUAGES)

    def test_get_news(self):
        """Test basic news retrieval with filters."""
        response = self.api.get_news(
            language='en',
            sport='football',
            size=5
        )
        
        self.assertIn('items', response)
        self.assertIn('total', response)
        self.assertIn('page', response)
        self.assertIn('size', response)
        
        if response['items']:
            for article in response['items']:
                self.validate_article(article)
                self.assertEqual(article['sport'], 'football')
                self.assertEqual(article['language'], 'en')

    def test_date_validation(self):
        """Test date filtering functionality."""
        from_date = datetime.now() - timedelta(days=7)
        response = self.api.get_news(from_date=from_date)
        self.assertIn('items', response)

        response = self.api.get_news(from_date='2024-01-01T00:00:00')
        self.assertIn('items', response)

    def test_pagination(self):
        """Test pagination limits and validation."""
        response = self.api.get_news(size=1000)
        self.assertLessEqual(response['size'], 100)
        
        response = self.api.get_news(size=-1)
        self.assertGreaterEqual(response['size'], 1)

    def test_invalid_language(self):
        """Test handling of invalid language parameter."""
        with self.assertRaises(ValueError) as context:
            self.api.get_news(language='invalid_language')
        self.assertIn("Invalid language code", str(context.exception))

    def test_invalid_sport(self):
        """Test handling of invalid sport parameter."""
        with self.assertRaises(ValueError) as context:
            self.api.get_news(sport='invalid_sport')
        self.assertIn("Invalid sport", str(context.exception))

    def test_error_handling(self):
        """Test API error handling."""
        # Test with invalid API key
        invalid_api = SportNewsAPI(api_key='invalid_key')
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_news()

        # Test with invalid endpoint
        invalid_endpoint_api = SportNewsAPI(
            api_key='sk_startup_6c1d8a80-4de6-4349-a479-f5be444ca6b9',
            base_url='https://nonexistent-api-endpoint.example.com'
        )
        with self.assertRaises(SportNewsAPIError):
            invalid_endpoint_api.get_news()

if __name__ == '__main__':
    unittest.main()