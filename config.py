import os
import json
import requests
import time
from datetime import datetime

def fetch_news():
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            raise Exception("API key not found in environment variables")

        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "token": api_key,
            "lang": "en",
            "country": "us",
            "max": 5  # 减少请求数量到5条
        }
        
        # 添加重试逻辑
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}: Fetching news from Gnews API...")
                response = requests.get(url, params=params, timeout=30)
                print(f"Response status: {response.status_code}")
                print(f"Response headers: {response.headers}")
                print(f"Response body: {response.text[:500]}...")  # 打印响应内容的前500个字符
                
                if response.status_code == 200:
                    data = response.json()
                    if not data.get('articles'):
                        print("No articles found in response")
                        continue
                        
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
                elif response.status_code == 429:  # Rate limit
                    print("Rate limit hit, waiting before retry...")
                    time.sleep(60)  # 等待60秒
                    continue
                else:
                    print(f"Error response: {response.text}")
                    if attempt == max_retries - 1:
                        raise Exception(f"API request failed with status {response.status_code}")
                    time.sleep(5)  # 等待5秒后重试
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)
                
        raise Exception("Failed to fetch news after all retries")
            
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
