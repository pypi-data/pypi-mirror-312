import unittest
from pathlib import Path
import sys
from datetime import datetime, timedelta
from typing import List

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews.client import SportNewsAPI, NewsArticle
from sportnews.exceptions import SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    def setUp(self):
        self.api = SportNewsAPI(
            api_key='sk_pro_5d24de40-c254-464c-85aa-09a3aeeb616e'
        )

    def validate_article(self, article: NewsArticle) -> None:
        """Vérifie la validité d'un objet NewsArticle"""
        # Vérifie d'abord la présence des attributs requis
        required_attributes = ['id', 'title', 'description', 'published', 'sport', 'language']
        for attr in required_attributes:
            self.assertTrue(hasattr(article, attr), f"L'article devrait avoir l'attribut {attr}")
        
        # Validation du contenu
        self.assertIsInstance(article.title, str)
        self.assertIsInstance(article.description, str)
        self.assertIsInstance(article.published, datetime)
        
        # Validation des longueurs de texte
        self.assertGreaterEqual(len(article.title), 3, "Le titre doit faire au moins 3 caractères")
        self.assertGreaterEqual(len(article.description), 10, "La description doit faire au moins 10 caractères")
        self.assertLessEqual(len(article.title), 500, "Le titre ne doit pas dépasser 500 caractères")
        self.assertLessEqual(len(article.description), 500, "La description ne doit pas dépasser 500 caractères")

        # Validation du format
        self.assertFalse(any(char in article.title for char in ['\n', '\r', '\t']))
        self.assertFalse(any(char in article.description for char in ['\n', '\r', '\t']))

    def test_get_latest_news(self):
        """Teste la récupération des dernières actualités"""
        articles = self.api.get_latest_news(limit=5, language='en')
        
        self.assertIsInstance(articles, list)
        self.assertLessEqual(len(articles), 5)
        
        if articles:
            for article in articles:
                self.validate_article(article)
                if article.language:
                    self.assertEqual(article.language, 'en')

    def test_search_news(self):
        """Teste la recherche d'actualités"""
        from_date = datetime.utcnow() - timedelta(days=7)
        articles = self.api.search_news(
            query="football",
            sport="football",
            language="en",
            from_date=from_date,
            limit=5
        )
        
        self.assertIsInstance(articles, list)
        self.assertLessEqual(len(articles), 5)
        
        if articles:
            for article in articles:
                self.validate_article(article)
                self.assertEqual(article.sport, 'football')
                self.assertEqual(article.language, 'en')

    def test_get_sport_news(self):
        """Teste la récupération des actualités par sport"""
        articles = self.api.get_sport_news(
            sport="football",
            language="en",
            limit=5
        )
        
        self.assertIsInstance(articles, list)
        self.assertLessEqual(len(articles), 5)
        
        if articles:
            for article in articles:
                self.validate_article(article)
                self.assertEqual(article.sport, 'football')
                self.assertEqual(article.language, 'en')

    def test_language_validation(self):
        """Teste la validation des codes de langue"""
        with self.assertRaises(ValueError) as context:
            self.api.get_latest_news(language='invalid_language')
        self.assertIn("Invalid language code", str(context.exception))

    def test_newsarticle_creation(self):
        """Teste la création d'objets NewsArticle"""
        test_data = {
            'id': '123',
            'title': 'Test Article',
            'description': 'This is a test article description',
            'published': datetime.now().isoformat(),
            'sport': 'football',
            'language': 'en',
            'author': 'Test Author',
            'link': 'http://test.com'
        }
        
        article = NewsArticle.from_dict(test_data)
        self.validate_article(article)
        self.assertEqual(article.id, '123')
        self.assertEqual(article.author, 'Test Author')
        self.assertEqual(article.link, 'http://test.com')

    def test_error_handling(self):
        """Teste la gestion des erreurs"""
        invalid_api = SportNewsAPI(
            api_key='invalid_key',
            base_url='http://invalid-url'
        )
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_latest_news()

if __name__ == '__main__':
    unittest.main()