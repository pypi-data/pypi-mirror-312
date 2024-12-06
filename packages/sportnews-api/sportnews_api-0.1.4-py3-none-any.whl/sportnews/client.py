import requests
import re
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
        """Valide et ajuste la taille de la page"""
        return max(self.MIN_PAGE_SIZE, min(size, self.MAX_PAGE_SIZE))

    def _clean_text(self, text: str) -> str:
        """Nettoie et normalise le texte"""
        if not isinstance(text, str):
            return ""
        # Supprime les caractères spéciaux et normalise les espaces
        text = re.sub(r'[\r\n\t"]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()[:500]

    def _format_date(self, date_value: Any) -> str:
        """Formate et valide la date"""
        try:
            if isinstance(date_value, str):
                date_obj = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            elif isinstance(date_value, datetime):
                date_obj = date_value
            else:
                return datetime.now().isoformat()
            return date_obj.isoformat()
        except:
            return datetime.now().isoformat()

    def _validate_article(self, article: Dict[str, Any], sport: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Valide et nettoie un article"""
        if not article or not isinstance(article, dict):
            return None

        title = article.get('title', '').strip()
        description = article.get('description', '').strip()
        published = article.get('published')
        
        if not title or not description or not published:
            return None

        cleaned_article = {
            'id': article.get('id', ''),
            'title': self._clean_text(title),
            'description': self._clean_text(description),
            'published': self._format_date(published),
            'author': self._clean_text(article.get('author', '')),
            'language': article.get('language', '').lower(),
            'sport': sport or article.get('sport', '').lower(),
            'link': article.get('link', '')
        }

        if len(cleaned_article['title']) < 3 or len(cleaned_article['description']) < 10:
            return None

        return cleaned_article

    def get_news(self, language: Optional[str] = None, page: int = 1, size: int = 10) -> Dict[str, Any]:
        """Récupère les actualités générales"""
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
        valid_articles = []
        for item in response.get('items', []):
            validated_article = self._validate_article(item)
            if validated_article:
                valid_articles.append(validated_article)

        return {
            'items': valid_articles,
            'total': len(valid_articles),
            'page': page,
            'size': size
        }

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
            params['from_date'] = self._format_date(from_date)
        if to_date:
            params['to_date'] = self._format_date(to_date)

        response = self._make_request('GET', endpoint, params=params)
        valid_articles = []
        for item in response.get('items', []):
            validated_article = self._validate_article(item, sport)
            if validated_article:
                valid_articles.append(validated_article)

        return {
            'items': valid_articles,
            'total': len(valid_articles),
            'page': page,
            'size': size
        }

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

        valid_articles = []
        for article in articles:
            if isinstance(article, dict):
                article['sport'] = sport
                validated_article = self._validate_article(article, sport)
                if validated_article:
                    valid_articles.append(validated_article)

        return {
            'items': valid_articles,
            'total': len(valid_articles)
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