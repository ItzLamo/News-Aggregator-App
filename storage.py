import json
from datetime import datetime
from typing import List, Dict

class Storage:
    def __init__(self):
        self.saved_articles_file = "saved_articles.json"
        self.search_history_file = "search_history.json"
        self.saved_articles = self.load_saved_articles()
        self.search_history = self.load_search_history()

    def load_saved_articles(self) -> List[Dict]:
        try:
            with open(self.saved_articles_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_search_history(self) -> List[Dict]:
        try:
            with open(self.search_history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_article(self, article: Dict) -> None:
        if article not in self.saved_articles:
            self.saved_articles.append(article)
            with open(self.saved_articles_file, 'w') as f:
                json.dump(self.saved_articles, f, indent=2)

    def save_search(self, query: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.search_history.append({"query": query, "timestamp": timestamp})
        with open(self.search_history_file, 'w') as f:
            json.dump(self.search_history, f, indent=2)

    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        return self.search_history[-limit:]