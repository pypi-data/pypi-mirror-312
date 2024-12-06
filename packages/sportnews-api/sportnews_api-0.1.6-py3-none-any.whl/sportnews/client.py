import requests
from datetime import datetime
from typing import Optional, Dict, Any
from .exceptions import SportNewsAPIError

class SportNewsAPI:
    """
    Client for interacting with the SportNews API.
    
    This class provides methods to retrieve sports news articles with various filtering options.
    """
    
    VALID_LANGUAGES = ['en', 'fr', 'es', 'it', 'de']
    VALID_SPORTS = [
        "football", "basketball", "tennis", "formula1", "cricket",
        "rugby", "golf", "boxing", "cycling", "mma", "nfl", "nhl",
        "athletics", "esports", "winter_sports", "volleyball",
        "handball", "motorsports", "water_sports"
    ]
    DEFAULT_API_URL = "https://fastapi-app-505935705476.northamerica-northeast1.run.app/api/v1"
    
    def __init__(self, api_key: str, base_url: str = None):
        """
        Initialize the SportNews API client.
        
        Args:
            api_key: API key for authentication
            base_url: Optional custom API base URL
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
        from_date: Optional[str | datetime] = None,
        to_date: Optional[str | datetime] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve sports news articles with filtering options.
        
        Args:
            language: Language code ('fr', 'en', 'es', 'it', 'de')
            sport: Specific sport (see VALID_SPORTS for complete list)
            from_date: Start date (ISO format or datetime object)
            to_date: End date (ISO format or datetime object)
            page: Page number for pagination
            size: Number of articles per page (1-100)
        
        Returns:
            Dict containing articles and pagination metadata
            
        Raises:
            SportNewsAPIError: If the API request fails
            ValueError: If invalid parameters are provided
        """
        if language and language not in self.VALID_LANGUAGES:
            raise ValueError(f"Invalid language code. Must be one of: {', '.join(self.VALID_LANGUAGES)}")
        
        if sport and sport not in self.VALID_SPORTS:
            raise ValueError(f"Invalid sport. Must be one of: {', '.join(self.VALID_SPORTS)}")

        if isinstance(from_date, datetime):
            from_date = from_date.isoformat()
        if isinstance(to_date, datetime):
            to_date = to_date.isoformat()
            
        endpoint = f"{self.base_url}/news"
        params = {
            'page': page,
            'size': min(max(1, size), 100)
        }
        
        if language:
            params['language'] = language
        if sport:
            params['sport'] = sport
        if from_date:
            params['from_date'] = from_date
        if to_date:
            params['to_date'] = to_date
            
        response = self._make_request('GET', endpoint, params=params)
        return self._process_response(response, sport)
    
    def _process_response(self, response: Dict[str, Any], sport: Optional[str] = None) -> Dict[str, Any]:
        """
        Process the API response and filter results if needed.
        
        Args:
            response: Raw API response
            sport: Sport to filter by (optional)
            
        Returns:
            Processed response with filtered items
        """
        items = response.get('items', [])
        if sport:
            items = [item for item in items if item.get('sport', '').lower() == sport.lower()]
            
        return {
            'items': items,
            'total': len(items),
            'page': response.get('page', 1),
            'size': response.get('size', len(items))
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
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