import requests
import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from .exceptions import SportNewsAPIError

@dataclass
class NewsArticle:
    """Représentation d'un article d'actualité sportive"""
    id: str
    title: str
    description: str
    published: datetime
    sport: str
    language: str
    author: Optional[str] = None
    link: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['NewsArticle']:
        """
        Crée une instance d'Article à partir d'un dictionnaire.
        Retourne None si les données ne sont pas valides.
        """
        try:
            # Validation des champs requis
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            published = data.get('published')
            sport = data.get('sport', '').strip()
            language = data.get('language', '').strip()

            # Vérification des critères minimaux
            if len(title) < 3 or len(description) < 10:
                return None

            # Nettoyage des textes
            title = re.sub(r'[\r\n\t"]', ' ', title)
            title = re.sub(r'\s+', ' ', title).strip()[:500]
            description = re.sub(r'[\r\n\t"]', ' ', description)
            description = re.sub(r'\s+', ' ', description).strip()[:500]

            # Conversion de la date
            if isinstance(published, str):
                published = datetime.fromisoformat(published.replace('Z', '+00:00'))
            elif not isinstance(published, datetime):
                published = datetime.now()

            return cls(
                id=data.get('id', ''),
                title=title,
                description=description,
                published=published,
                sport=sport.lower(),
                language=language.lower(),
                author=data.get('author'),
                link=data.get('link')
            )
        except Exception:
            return None

class SportNewsAPI:
    """Client API pour accéder aux actualités sportives"""
    
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

    def _validate_language(self, language: Optional[str]) -> None:
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")

    def _process_response(self, response: Dict[str, Any], sport: Optional[str] = None) -> List[NewsArticle]:
        if isinstance(response, list):
            items = response
        else:
            items = response.get('items', [])

        articles = []
        for item in items:
            if isinstance(item, dict):
                if sport:
                    item['sport'] = sport
                article = NewsArticle.from_dict(item)
                if article:
                    articles.append(article)
        return articles

    def get_latest_news(self, limit: int = 10, language: Optional[str] = None) -> List[NewsArticle]:
        self._validate_language(language)
        
        params = {'size': min(max(limit, self.MIN_PAGE_SIZE), self.MAX_PAGE_SIZE)}
        if language:
            params['language'] = language

        response = self._make_request('GET', f"{self.base_url}/news", params=params)
        return self._process_response(response)

    def get_sport_news(self, sport: str, language: Optional[str] = None, limit: int = 5) -> List[NewsArticle]:
        self._validate_language(language)

        params = {'limit': min(max(limit, 1), 50)}
        if language:
            params['language'] = language

        response = self._make_request('GET', f"{self.base_url}/news/latest/{sport}", params=params)
        return self._process_response(response, sport)

    def search_news(self, query: str, sport: Optional[str] = None, language: Optional[str] = None,
                   from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                   limit: int = 10) -> List[NewsArticle]:
        self._validate_language(language)

        params = {
            'query': query,
            'size': min(max(limit, self.MIN_PAGE_SIZE), self.MAX_PAGE_SIZE)
        }
        if language:
            params['language'] = language
        if sport:
            params['sport'] = sport
        if from_date:
            params['from_date'] = from_date.isoformat()
        if to_date:
            params['to_date'] = to_date.isoformat()

        response = self._make_request('GET', f"{self.base_url}/news/search", params=params)
        return self._process_response(response, sport)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SportNewsAPIError(f"API request failed: {str(e)}")