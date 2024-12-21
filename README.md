# News Aggregator App

A simple Python app that aggregates news articles based on user preferences. It allows users to search for news articles, view them in their browser, and save articles for later.

## Features

- Search news by keywords or categories like technology, sports, health, etc.
- View full articles in the browser.
- Save articles for later viewing.
- View search history.

## Requirements

- Python 3.x
- `requests` library (for handling HTTP requests)
- `tkinter` (for the GUI)

## Setup Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone [https://github.com/ItzLamo/News-Aggregator-App]
   cd news-aggregator-app
   ```

2. Install the required Python libraries:

   ```bash
   pip install requests
   ```

3. Obtain a free API key from [NewsAPI](https://newsapi.org/). Replace `"your_api_key_here"` in the `NewsAPI` class in the code with your key.

4. Run the app using the following command:

   ```bash
   python app.py
   ```
