import requests
from typing import Optional, List, Dict, Any
from datetime import datetime
from .exceptions import SportNewsAPIError
from .models import NewsArticle

class SportNewsAPI:
    VALID_LANGUAGES = ['en', 'fr', 'es', 'it', 'de']
    DEFAULT_API_URL = "https://fastapi-app-505935705476.northamerica-northeast1.run.app/api/v1"
    MIN_PAGE_SIZE = 1
    MAX_PAGE_SIZE = 100
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_API_URL).rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })

    def _validate_page_size(self, size: int) -> int:
        return max(self.MIN_PAGE_SIZE, min(size, self.MAX_PAGE_SIZE))

    def _convert_to_dict(self, article: NewsArticle) -> Dict[str, Any]:
        return {
            'id': article.id,
            'title': article.title,
            'link': article.link,
            'published': article.published.isoformat(),
            'description': article.description,
            'author': article.author,
            'language': article.language,
            'sport': article.sport
        }

    def get_news(self, language: Optional[str] = None, page: int = 1, size: int = 10) -> Dict[str, Any]:
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

        endpoint = f"{self.base_url}/news"
        params = {
            'page': page,
            'size': self._validate_page_size(size)
        }
        if language:
            params['language'] = language

        response = self._make_request('GET', endpoint, params=params)
        articles = [NewsArticle.from_dict(item) for item in response['items']]
        response['items'] = [self._convert_to_dict(article) for article in articles]
        return response

    def search_news(
        self,
        query: str,
        sport: Optional[str] = None,
        language: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

        endpoint = f"{self.base_url}/news/search"
        params = {
            'query': query,
            'page': page,
            'size': self._validate_page_size(size)
        }
        if language:
            params['language'] = language
        if sport:
            params['sport'] = sport
        if from_date:
            params['from_date'] = from_date.isoformat()
        if to_date:
            params['to_date'] = to_date.isoformat()

        response = self._make_request('GET', endpoint, params=params)
        articles = [NewsArticle.from_dict(item) for item in response['items']]
        response['items'] = [self._convert_to_dict(article) for article in articles]
        return response

    def get_latest_sport_news(
        self,
        sport: str,
        language: Optional[str] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

        endpoint = f"{self.base_url}/news/latest/{sport}"
        params = {
            'limit': max(1, min(limit, 50))
        }
        if language:
            params['language'] = language

        response = self._make_request('GET', endpoint, params=params)
        if isinstance(response, list):
            articles = response
        else:
            articles = response.get('items', [])
            
        for article in articles:
            if isinstance(article, dict):
                article['sport'] = sport
        
        article_objects = [NewsArticle.from_dict(item) for item in articles]
        return {
            'items': [self._convert_to_dict(article) for article in article_objects],
            'total': len(article_objects)
        }

    def get_cache_status(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/news/cache/status"
        return self._make_request('GET', endpoint)

    def clear_cache(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/news/cache/clear"
        return self._make_request('DELETE', endpoint)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SportNewsAPIError(f"API request failed: {str(e)}")