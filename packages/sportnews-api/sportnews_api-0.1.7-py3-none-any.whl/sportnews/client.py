# src/sportnews/client.py
import requests
from datetime import datetime
from typing import Optional, Dict, Any, Union
from .exceptions import SportNewsAPIError

class SportNewsAPI:
    """
    Client for the SportNews API service.
    
    Provides methods to retrieve sports news articles with various filtering options
    including language, sport type, and date ranges.
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
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve sports news articles with filtering options.
        
        Args:
            language: Language code for articles (e.g., 'en', 'fr')
            sport: Sport category to filter by
            from_date: Start date for article search
            to_date: End date for article search
            page: Page number for pagination
            size: Number of articles per page (max 100)
            
        Returns:
            Dictionary containing articles and pagination metadata
            
        Raises:
            SportNewsAPIError: If the API request fails
            ValueError: If invalid parameters are provided
        """
        self._validate_parameters(language, sport)
        
        params = self._prepare_request_params(
            language, sport, from_date, to_date, page, size
        )
        
        endpoint = f"{self.base_url}/news"
        response = self._make_request('GET', endpoint, params=params)
        return self._process_response(response, sport)
    
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
    
    def _prepare_request_params(
        self,
        language: Optional[str],
        sport: Optional[str],
        from_date: Optional[Union[str, datetime]],
        to_date: Optional[Union[str, datetime]],
        page: int,
        size: int
    ) -> Dict[str, Any]:
        """Prepare request parameters."""
        params = {
            'page': page,
            'size': min(max(1, size), 100)
        }
        
        if isinstance(from_date, datetime):
            from_date = from_date.isoformat()
        if isinstance(to_date, datetime):
            to_date = to_date.isoformat()
        
        optional_params = {
            'language': language,
            'sport': sport,
            'from_date': from_date,
            'to_date': to_date
        }
        
        params.update({k: v for k, v in optional_params.items() if v is not None})
        return params
    
    def _process_response(
        self,
        response: Dict[str, Any],
        sport: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process and format API response."""
        items = response.get('items', [])
        if sport:
            items = [
                item for item in items
                if item.get('sport', '').lower() == sport.lower()
            ]
        
        return {
            'items': items,
            'total': len(items),
            'page': response.get('page', 1),
            'size': response.get('size', len(items))
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to the API.
        
        Args:
            method: HTTP method to use
            endpoint: API endpoint URL
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