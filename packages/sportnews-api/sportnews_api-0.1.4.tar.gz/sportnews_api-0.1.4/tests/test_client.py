import unittest
from pathlib import Path
import sys
import os
from datetime import datetime, timedelta
import re

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews import SportNewsAPI, SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    def setUp(self):
        self.api = SportNewsAPI(
            api_key='sk_pro_5d24de40-c254-464c-85aa-09a3aeeb616e'
        )

    def validate_text_content(self, text):
        """Vérifie que le texte respecte les règles de nettoyage"""
        self.assertIsInstance(text, str)
        self.assertLessEqual(len(text), 500)
        self.assertFalse(any(char in text for char in ['\n', '\r', '\t']))
        self.assertFalse(re.search(r'\s{2,}', text))

    def validate_date_format(self, date_str):
        """Vérifie que la date est au format ISO"""
        self.assertIsInstance(date_str, str)
        try:
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            self.fail("Date format invalide")

    def validate_article_structure(self, article):
        """Vérifie la structure complète d'un article"""
        required_fields = ['id', 'title', 'description', 'published', 'sport', 'language']
        for field in required_fields:
            self.assertIn(field, article)
        
        self.validate_text_content(article['title'])
        self.validate_text_content(article['description'])
        self.validate_date_format(article['published'])
        self.assertGreaterEqual(len(article['title']), 3)
        self.assertGreaterEqual(len(article['description']), 10)
        self.assertIn(article['language'], self.api.VALID_LANGUAGES)

    def test_get_news(self):
        news_response = self.api.get_news(language='en', page=1, size=10)
        
        self.assertIn('total', news_response)
        self.assertIn('items', news_response)
        self.assertIsInstance(news_response['items'], list)
        
        if news_response['items']:
            for article in news_response['items']:
                self.validate_article_structure(article)

    def test_search_news(self):
        search_results = self.api.search_news(
            query="football",
            from_date=datetime.utcnow() - timedelta(days=7),
            language="en",
            sport="football",
            size=5
        )
        
        self.assertIn('items', search_results)
        self.assertLessEqual(len(search_results['items']), 5)
        
        if search_results['items']:
            for article in search_results['items']:
                self.validate_article_structure(article)
                self.assertEqual(article['sport'], 'football')
                self.assertEqual(article['language'], 'en')

    def test_get_latest_sport_news(self):
        sport_news = self.api.get_latest_sport_news(
            sport="football",
            language="en",
            limit=5
        )
        
        self.assertIsInstance(sport_news, dict)
        self.assertIn('items', sport_news)
        self.assertLessEqual(len(sport_news['items']), 5)
        
        if sport_news['items']:
            for article in sport_news['items']:
                self.validate_article_structure(article)
                self.assertEqual(article['sport'], 'football')
                self.assertEqual(article['language'], 'en')

    def test_text_cleaning(self):
        """Tests spécifiques pour le nettoyage des textes"""
        dirty_text = "Test\nwith\tmultiple    spaces\rand\tspecial\ncharacters"
        cleaned_text = self.api._clean_text(dirty_text)
        self.assertEqual(cleaned_text, "Test with multiple spaces and special characters")
        
        long_text = "a" * 600
        cleaned_long_text = self.api._clean_text(long_text)
        self.assertEqual(len(cleaned_long_text), 500)

    def test_date_formatting(self):
        """Tests spécifiques pour le formatage des dates"""
        test_date = datetime.now()
        formatted_date = self.api._format_date(test_date)
        self.validate_date_format(formatted_date)
        
        invalid_date = "invalid_date"
        fallback_date = self.api._format_date(invalid_date)
        self.validate_date_format(fallback_date)

    def test_article_validation(self):
        """Tests spécifiques pour la validation des articles"""
        invalid_article = {
            'title': 'Te',  # Trop court
            'description': 'Too short',  # Trop court
            'published': datetime.now(),
            'sport': 'football'
        }
        validated = self.api._validate_article(invalid_article)
        self.assertIsNone(validated)
        
        valid_article = {
            'title': 'Valid Title',
            'description': 'This is a valid description that meets the minimum length requirement',
            'published': datetime.now(),
            'sport': 'football',
            'language': 'en'
        }
        validated = self.api._validate_article(valid_article)
        self.assertIsNotNone(validated)
        self.validate_article_structure(validated)

    def test_invalid_language(self):
        with self.assertRaises(ValueError) as context:
            self.api.get_news(language='invalid_language')
        self.assertIn("Invalid language code", str(context.exception))

    def test_error_handling(self):
        invalid_api = SportNewsAPI(
            api_key='invalid_key',
            base_url='http://invalid-url'
        )
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_news()

if __name__ == '__main__':
    unittest.main()