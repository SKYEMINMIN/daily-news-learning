import os
import json
import requests
from datetime import datetime

def fetch_news():
    try:
        api_key = os.environ.get('NEWS_API_KEY')  # 我们暂时使用同样的环境变量名
        if not api_key:
            raise Exception("API key not found in environment variables")

        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "lang": "en",      # 英文新闻
            "country": "us",   # 美国新闻
            "max": 10,         # 获取10条新闻
            "apikey": api_key
        }
        
        print(f"Fetching news from Gnews API...")
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # 转换为与原格式兼容的结构
            formatted_data = {
                "status": "ok",
                "articles": [{
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "urlToImage": article.get("image"),
                    "publishedAt": article["publishedAt"],
                    "source": {"name": article["source"]["name"]}
                } for article in data["articles"]]
            }
            return formatted_data
        else:
            print(f"Error response: {response.text}")
            raise Exception(f"API request failed with status {response.status_code}")
            
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
