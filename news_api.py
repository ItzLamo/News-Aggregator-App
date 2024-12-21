import json
from datetime import datetime, timedelta
import requests
from typing import List, Dict

class NewsAPI:
    def __init__(self):
        self.api_key = "a886a96e188e4591bcff3342547fe6eb"  # Ensure this is the correct key
        self.base_url = "https://newsapi.org/v2/"
        self.categories = [
            "business", "entertainment", "general", "health", 
            "science", "sports", "technology"
        ]

    def fetch_news(self, keywords: str = "", category: str = None, days: int = 7) -> List[Dict]:
        try:
            # Prepare URL and parameters based on search type
            if category and category in self.categories:
                url = f"{self.base_url}top-headlines"
                params = {
                    'category': category,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'pageSize': 15
                }
            else:
                url = f"{self.base_url}everything"
                params = {
                    'q': keywords,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'pageSize': 15,
                    'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
                }

            # Set Authorization headers
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            # Make the request using requests library
            response = requests.get(url, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()  # Convert the response to a JSON object
                return self._format_articles(data.get('articles', []))
            else:
                print(f"Error fetching news: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def _format_articles(self, articles: List[Dict]) -> List[Dict]:
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.get('title', 'No title'),
                'source': article.get('source', {}).get('name', 'Unknown source'),
                'description': article.get('description', 'No description'),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'author': article.get('author', 'Unknown author'),
                'content': article.get('content', 'No content available')
            })
        return formatted_articles
