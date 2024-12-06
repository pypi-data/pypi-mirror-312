from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class NewsArticle:
    """Represents a news article from the Sport News API."""
    
    id: str = ''
    title: str = ''
    link: str = ''
    published: datetime = datetime.utcnow()
    description: str = ''
    author: str = 'Unknown'
    language: str = 'en'
    sport: str = ''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NewsArticle':
        """
        Create a NewsArticle instance from a dictionary.
        
        Args:
            data: Dictionary containing article data
            
        Returns:
            NewsArticle: Instance populated with the provided data
        """
        processed_data = {
            'id': data.get('id', ''),
            'title': data.get('title', ''),
            'link': data.get('link', ''),
            'description': data.get('description', ''),
            'author': data.get('author', 'Unknown'),
            'language': data.get('language', 'en'),
            'sport': data.get('sport', '')
        }

        # Handle published date
        published = data.get('published')
        if isinstance(published, str):
            try:
                processed_data['published'] = datetime.fromisoformat(published.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                processed_data['published'] = datetime.utcnow()
        else:
            processed_data['published'] = datetime.utcnow()

        return cls(**processed_data)