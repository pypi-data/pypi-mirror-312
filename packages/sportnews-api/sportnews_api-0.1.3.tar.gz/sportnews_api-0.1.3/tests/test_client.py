import unittest
from pathlib import Path
import sys
import os
from datetime import datetime, timedelta

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from sportnews import SportNewsAPI, SportNewsAPIError

class TestSportNewsAPI(unittest.TestCase):
    def setUp(self):
        self.api = SportNewsAPI(
            api_key='sk_pro_5d24de40-c254-464c-85aa-09a3aeeb616e'
        )

    def test_get_news(self):
        news_response = self.api.get_news(language='en', page=1, size=10)
        
        self.assertIn('total', news_response)
        self.assertIn('items', news_response)
        self.assertIn('page', news_response)
        self.assertIn('size', news_response)
        
        if news_response['items']:
            article = news_response['items'][0]
            self.assertIsInstance(article['id'], str)
            self.assertIsInstance(article['title'], str)
            self.assertIsInstance(article['link'], str)
            self.assertIsInstance(article['published'], str)
            self.assertIsInstance(article['description'], str)
            self.assertIsInstance(article['author'], str)
            self.assertIsInstance(article['language'], str)
            self.assertIsInstance(article['sport'], str)
            
            print(f"\nGeneral News Article Details:")
            print(f"Title: {article['title']}")
            print(f"Published: {article['published']}")
            print(f"Description: {article['description']}")
            print(f"Sport: {article['sport']}")
            print(f"Language: {article['language']}")

    def test_search_news(self):
        search_results = self.api.search_news(
            query="football",
            from_date=datetime.utcnow() - timedelta(days=7),
            language="en",
            sport="football",
            size=5
        )
        
        self.assertIn('total', search_results)
        self.assertIn('items', search_results)
        self.assertIn('page', search_results)
        self.assertIn('size', search_results)
        self.assertLessEqual(len(search_results['items']), 5)
        
        if search_results['items']:
            article = search_results['items'][0]
            self.assertIsInstance(article['id'], str)
            self.assertIsInstance(article['title'], str)
            self.assertIsInstance(article['published'], str)
            self.assertIsInstance(article['sport'], str)

    def test_get_latest_sport_news(self):
        sport_news = self.api.get_latest_sport_news(
            sport="football",
            language="en",
            limit=5
        )
        
        self.assertIsInstance(sport_news, dict)
        self.assertIn('items', sport_news)
        self.assertIn('total', sport_news)
        self.assertLessEqual(len(sport_news['items']), 5)
        
        if sport_news['items']:
            article = sport_news['items'][0]
            self.assertIsInstance(article['id'], str)
            self.assertIsInstance(article['title'], str)
            self.assertIsInstance(article['link'], str)
            self.assertIsInstance(article['published'], str)
            self.assertIsInstance(article['description'], str)
            self.assertIsInstance(article['author'], str)
            self.assertEqual(article['sport'], "football")
            self.assertEqual(article['language'], "en")

    def test_cache_operations(self):
        cache_status = self.api.get_cache_status()
        self.assertIn('status', cache_status)
        self.assertIn('total_keys', cache_status)
        self.assertIn('keys_by_prefix', cache_status)
        self.assertIsInstance(cache_status['total_keys'], int)
        self.assertIsInstance(cache_status['keys_by_prefix'], dict)
        
        clear_result = self.api.clear_cache()
        self.assertIn('status', clear_result)
        self.assertIn('keys_deleted', clear_result)
        self.assertIn('timestamp', clear_result)
        self.assertIsInstance(clear_result['keys_deleted'], int)
        self.assertIsInstance(clear_result['timestamp'], str)

    def test_language_validation(self):
        with self.assertRaises(ValueError) as context:
            self.api.get_news(language='invalid_language')
        self.assertIn("Invalid language code", str(context.exception))

    def test_connection_error(self):
        invalid_api = SportNewsAPI(
            api_key='sk_startup_6c1d8a80-4de6-4349-a479-f5be444ca6b9',
            base_url='http://invalid-url'
        )
        with self.assertRaises(SportNewsAPIError):
            invalid_api.get_news()

    def test_pagination_limits(self):
        response = self.api.get_news(size=10)
        self.assertEqual(response['size'], 10)

        response = self.api.get_news(size=-1)
        self.assertEqual(response['size'], 1)

    def test_date_formatting(self):
        from_date = datetime.utcnow() - timedelta(days=7)
        search_results = self.api.search_news(
            query="test",
            from_date=from_date
        )
        self.assertIn('items', search_results)

    def test_invalid_api_key(self):
        invalid_api = SportNewsAPI('invalid_key')
        with self.assertRaises(SportNewsAPIError) as context:
            invalid_api.get_news()
        self.assertIn('401', str(context.exception))

    def test_response_validation(self):
        news_response = self.api.get_news()
        self.assertIsInstance(news_response, dict)
        self.assertIn('total', news_response)
        self.assertIsInstance(news_response['total'], int)
        self.assertGreaterEqual(news_response['total'], 0)

if __name__ == '__main__':
    unittest.main()