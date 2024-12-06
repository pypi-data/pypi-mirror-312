import requests
from datetime import datetime
from typing import Optional, Dict, Any, Union, List

class SportNewsAPIError(Exception):
    """Base exception class for SportNews API errors."""
    pass

class SportNewsAPI:
    """
    Client for the SportNews API service.
    Provides methods to retrieve and search sports news articles with various filtering options.
    """
    
    VALID_LANGUAGES = ['en', 'fr', 'es', 'it', 'de']
    VALID_SPORTS = [
        "football", "basketball", "tennis", "formula1", "cricket",
        "rugby", "golf", "boxing", "cycling", "mma", "nfl", "nhl",
        "athletics", "esports", "winter_sports", "volleyball",
        "handball", "motorsports", "water_sports"
    ]
    DEFAULT_API_URL = "https://fastapi-app-505935705476.northamerica-northeast1.run.app/api/v1"
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the SportNews API client.
        
        Args:
            api_key: Authentication key for the API
            base_url: Optional custom API endpoint URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_API_URL).rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })

    def get_news(
        self,
        language: Optional[str] = None,
        sport: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve sports news articles with basic filtering.
        
        Args:
            language: Language code for articles (e.g., 'en', 'fr')
            sport: Sport category to filter by
            page: Page number for pagination
            size: Number of articles per page (max 100)
            
        Returns:
            Dictionary containing articles and pagination metadata
        """
        self._validate_parameters(language, sport)
        
        endpoint = f"{self.base_url}/news"
        params = self._prepare_request_params(
            language=language,
            sport=sport,
            page=page,
            size=size
        )
        
        return self._make_request('GET', endpoint, params=params)

    def search_news(
        self,
        query: str,
        sport: Optional[str] = None,
        language: Optional[str] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Search for news articles with advanced filtering options.
        
        Args:
            query: Search term
            sport: Sport category filter
            language: Language code filter
            from_date: Start date for article search
            to_date: End date for article search
            page: Page number
            size: Results per page (max 100)
            
        Returns:
            Dictionary containing search results and metadata
        """
        self._validate_parameters(language, sport)
        
        endpoint = f"{self.base_url}/news/search"
        params = self._prepare_request_params(
            query=query,
            sport=sport,
            language=language,
            from_date=from_date,
            to_date=to_date,
            page=page,
            size=size
        )
        
        return self._make_request('GET', endpoint, params=params)

    def get_latest_sport_news(
        self,
        sport: str,
        language: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get latest news articles for a specific sport.
        
        Args:
            sport: Sport category
            language: Optional language filter
            limit: Number of articles to return (max 50)
            
        Returns:
            List of news articles
        """
        self._validate_parameters(language, sport)
        
        endpoint = f"{self.base_url}/news/latest/{sport}"
        params = {
            'language': language,
            'limit': min(max(1, limit), 50)
        }
        
        return self._make_request('GET', endpoint, params=params)

    def _validate_parameters(self, language: Optional[str], sport: Optional[str]) -> None:
        """Validate input parameters."""
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(
                f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}"
            )
        
        if sport and sport not in self.VALID_SPORTS:
            raise ValueError(
                f"Invalid sport. Must be one of: {', '.join(self.VALID_SPORTS)}"
            )

    def _prepare_request_params(self, **kwargs) -> Dict[str, Any]:
        """Prepare request parameters."""
        params = {}
        
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, datetime):
                    params[key] = value.isoformat()
                else:
                    params[key] = value
        
        if 'size' in params:
            params['size'] = min(max(1, params['size']), 100)
            
        return params

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to the API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            SportNewsAPIError: If the request fails
        """
        try:
            response = self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SportNewsAPIError(f"API request failed: {str(e)}") from e