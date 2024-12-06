
# SportNews API SDK

An official Python SDK for the SportNews API, providing streamlined access to real-time sports news. This library allows developers to easily integrate sports news feeds into their Python applications.

## Installation

```bash
pip install sportnews-api
```

## Usage

```python
from sportnews import SportNewsAPI

# Initialize the client with your API key
api = SportNewsAPI('YOUR_API_KEY')

# Retrieve the latest news
articles = api.get_news(language='fr', size=5)

print("Dernières actualités :")
if articles['items']:
    for article in articles['items']:
        print(f"Titre: {article['title']}")
        print(f"Date: {article['published']}")
        print(f"Description: {article['description']}")
        print(f"Sport: {article['sport']}")
        print("---")
else:
    print("Aucun article trouvé")
```

### Searching for Articles

```python
# Search for articles about football from the last 7 days

results = api.search_news(
    query="Champions League",
    sport="football",
    language="en",
    size=10
)

if results['items']:
    for article in results['items']:
        print(f"Titre: {article['title']}")
        print(f"Date: {article['published']}")
        print(f"Description: {article['description']}")
        print(f"Sport: {article['sport']}")
        print("---")
else:
    print("Aucun résultat trouvé")
```

## Key Features

- Retrieve the latest sports news
- Search articles with advanced filters
- Multilingual support (FR, EN, ES, IT, DE)
- Pagination of results
- Robust error handling
- Automatic parameter validation
- Date-based search for temporal filtering

## NewsArticle Object

Each news article returned by the API has the following attributes:
- `title` (str): The title of the article.
- `published` (datetime): The publication date.
- `description` (str): A brief summary of the article.
- `sport` (str): The sport associated with the article.
- `language` (str): The language of the article.

## Error Handling

The SDK raises a `SportNewsAPIError` for any issues during API requests. Make sure to handle these exceptions in your application:

```python
from sportnews import SportNewsAPI, SportNewsAPIError

try:
    news = api.get_latest_news(language='fr')
except SportNewsAPIError as e:
    print(f"An error occurred: {e}")
```

## Supported Languages

- French (`fr`)
- English (`en`)
- Spanish (`es`)
- Italian (`it`)
- German (`de`)

## License

This project is licensed under the MIT License.

## Running Tests

The SDK includes a suite of unit tests to validate its functionality. Run the following command to execute the tests:

```bash
python -m unittest discover tests
```

## Support

- Documentation: [https://docs.sportnews-api.com](https://docs.sportnews-api.com)
- Support email: support@sportnews-api.com

Developed and maintained by the SportNews API team.
