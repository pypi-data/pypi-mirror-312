import unittest
from datetime import datetime, timedelta
from pathlib import Path
import sys
from typing import Dict, Any

# Add project root to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews.client import SportNewsAPI
from sportnews.exceptions import SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    """Test suite for the SportNews API client."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = SportNewsAPI(
            api_key='sk_startup_6c1d8a80-4de6-4349-a479-f5be444ca6b9'
        )
        self.test_api_key = 'sk_startup_6c1d8a80-4de6-4349-a479-f5be444ca6b9'

    def validate_article(self, article: Dict[str, Any]) -> None:
        """
        Validate the structure and content of a news article.
        
        Args:
            article: Dictionary containing article data
        """
        # Check required fields
        required_fields = ['title', 'description', 'published', 'sport', 'language']
        for field in required_fields:
            self.assertIn(
                field, 
                article, 
                f"Required field '{field}' is missing from article"
            )

        # Validate types
        self.assertIsInstance(article['title'], str, "Title must be a string")
        self.assertIsInstance(article['description'], str, "Description must be a string")

        # Validate content length
        self.assertGreaterEqual(len(article['title']), 3, "Title is too short")
        self.assertGreaterEqual(len(article['description']), 10, "Description is too short")
        self.assertLessEqual(len(article['title']), 500, "Title is too long")
        self.assertLessEqual(len(article['description']), 500, "Description is too long")

        # Check for invalid characters
        invalid_chars = ['\n', '\r', '\t']
        for char in invalid_chars:
            self.assertFalse(
                char in article['title'],
                f"Title contains invalid character: {repr(char)}"
            )
            self.assertFalse(
                char in article['description'],
                f"Description contains invalid character: {repr(char)}"
            )

        # Validate sport and language values if present
        if article['sport']:
            self.assertIn(
                article['sport'],
                self.api.VALID_SPORTS,
                f"Invalid sport: {article['sport']}"
            )
        if article['language']:
            self.assertIn(
                article['language'],
                self.api.VALID_LANGUAGES,
                f"Invalid language: {article['language']}"
            )

    def test_initialization(self):
        """Test client initialization with various parameters."""
        # Test with default base URL
        api = SportNewsAPI(api_key=self.test_api_key)
        self.assertEqual(api.base_url, self.api.DEFAULT_API_URL)

        # Test with custom base URL
        custom_url = "https://custom-api-url.com"
        api = SportNewsAPI(api_key=self.test_api_key, base_url=custom_url)
        self.assertEqual(api.base_url, custom_url)

        # Test URL trailing slash handling
        api = SportNewsAPI(api_key=self.test_api_key, base_url=custom_url + '/')
        self.assertEqual(api.base_url, custom_url)

    def test_get_news_basic(self):
        """Test basic news retrieval functionality."""
        response = self.api.get_news(
            language='en',
            sport='football',
            size=5
        )

        # Validate response structure
        self.assertIn('items', response)
        self.assertIn('total', response)
        self.assertIn('page', response)
        self.assertIn('size', response)

        # Validate response content
        self.assertLessEqual(len(response['items']), 5)
        
        if response['items']:
            for article in response['items']:
                self.validate_article(article)
                self.assertEqual(article['sport'], 'football')
                self.assertEqual(article['language'], 'en')

    def test_date_filtering(self):
        """Test date-based filtering of news articles."""
        # Test with datetime object
        from_date = datetime.now() - timedelta(days=7)
        response = self.api.get_news(from_date=from_date)
        self.assertIn('items', response)

        # Test with ISO format string
        response = self.api.get_news(from_date='2024-01-01T00:00:00')
        self.assertIn('items', response)

        # Test date range
        to_date = datetime.now()
        response = self.api.get_news(
            from_date=from_date,
            to_date=to_date
        )
        self.assertIn('items', response)

    def test_pagination(self):
        """Test pagination functionality and limits."""
        # Test maximum size limit
        response = self.api.get_news(size=1000)
        self.assertLessEqual(response['size'], 100)

        # Test minimum size limit
        response = self.api.get_news(size=-1)
        self.assertGreaterEqual(response['size'], 1)

        # Test multiple pages
        page1 = self.api.get_news(page=1, size=5)
        page2 = self.api.get_news(page=2, size=5)
        
        if page1['items'] and page2['items']:
            self.assertNotEqual(
                page1['items'][0]['title'],
                page2['items'][0]['title']
            )

    def test_language_validation(self):
        """Test language parameter validation."""
        # Test invalid language
        with self.assertRaises(ValueError) as context:
            self.api.get_news(language='invalid_language')
        self.assertIn("Invalid language code", str(context.exception))

        # Test all valid languages
        for lang in self.api.VALID_LANGUAGES:
            response = self.api.get_news(language=lang)
            self.assertIn('items', response)

    def test_sport_validation(self):
        """Test sport parameter validation."""
        # Test invalid sport
        with self.assertRaises(ValueError) as context:
            self.api.get_news(sport='invalid_sport')
        self.assertIn("Invalid sport", str(context.exception))

        # Test all valid sports
        for sport in self.api.VALID_SPORTS:
            response = self.api.get_news(sport=sport)
            self.assertIn('items', response)

    def test_error_handling(self):
        """Test API error handling scenarios."""
        # Test with invalid API key
        invalid_api = SportNewsAPI(api_key='invalid_key')
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_news()

        # Test with invalid endpoint
        invalid_endpoint_api = SportNewsAPI(
            api_key=self.test_api_key,
            base_url='https://nonexistent-api-endpoint.example.com'
        )
        with self.assertRaises(SportNewsAPIError):
            invalid_endpoint_api.get_news()

if __name__ == '__main__':
    unittest.main()