import os
import json
import requests
from datetime import datetime

def fetch_news():
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        raise Exception("NEWS_API_KEY not found in environment variables")
    
    # 打印 API key 的前几个字符（安全起见不打印完整的）
    print(f"Using API key starting with: {api_key[:5]}...")
    
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        "apiKey": api_key
    }
    
    try:
        print(f"Requesting URL: {url}")
        response = requests.get(url, params=params)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json() if response.text else "No error detail available"
            print(f"API Error Response: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
    except Exception as e:
        print(f"Error in fetch_news: {str(e)}")
        raise

def save_news(news_data):
    os.makedirs('data', exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/news-{today}.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"News data saved to {filename}")
    except Exception as e:
        print(f"Error saving news data: {str(e)}")
        raise

def main():
    try:
        print("Starting news fetch process...")
        print(f"Current environment variables: {list(os.environ.keys())}")
        news_data = fetch_news()
        
        if news_data and 'articles' in news_data:
            print(f"Retrieved {len(news_data['articles'])} articles")
            save_news(news_data)
            print("News update completed successfully!")
        else:
            raise Exception("No articles found in API response")
            
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
