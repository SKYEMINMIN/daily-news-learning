import requests
import json
import os
from datetime import datetime
import pytz
import time

API_KEY = '70c47808e1fc40f2bb4450e822b5f2fc'
BASE_URL = 'https://newsapi.org/v2/everything'

def search_news(query):
    """
    使用 NewsAPI 获取新闻
    """
    try:
        headers = {
            'X-Api-Key': API_KEY,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 5,  # 获取5条新闻
            'domains': 'bbc.com,cnn.com,reuters.com,theguardian.com,apnews.com,npr.org,washingtonpost.com'
        }
        
        print(f"Fetching news for query: {query}")  # 调试日志
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
        print(f"Response status: {response.status_code}")  # 调试日志
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")  # 打印错误响应
            return None
            
        data = response.json()
        print(f"API response: {data.get('status')}")  # 调试日志
        
        if data.get('status') == 'ok' and data.get('articles'):
            # 遍历文章列表，找到第一个有效的新闻
            for article in data['articles']:
                if article.get('title') and article.get('url'):
                    news = {
                        "title": article['title'],
                        "url": article['url'],
                        "source": article.get('source', {}).get('name', 'Unknown source'),
                        "time": article.get('publishedAt', datetime.now().isoformat())
                    }
                    print(f"Found news: {news}")  # 调试日志
                    return news
            print(f"No valid articles found for query: {query}")
            return None
        else:
            print(f"No articles found for query: {query}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def save_news_json(news_data):
    """
    保存新闻数据到JSON文件
    """
    try:
        os.makedirs('data', exist_ok=True)
        
        output = {
            "metadata": {
                "last_updated": datetime.now(pytz.UTC).isoformat()
            },
            "news": news_data
        }
        
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"News data saved successfully")
        print(f"Saved content: {json.dumps(output, indent=2)}")  # 打印保存的内容
        
    except Exception as e:
        print(f"Error saving news data: {str(e)}")

def main():
    queries = {
        'ai': 'artificial intelligence technology',
        'entertainment': 'entertainment OR movies OR music',
        'finance': 'finance OR business OR market',
        'politics': 'politics OR government'
    }
    
    news_data = {}
    success = False
    
    for category, query in queries.items():
        print(f"\nProcessing category: {category}")
        for attempt in range(3):  # 添加重试机制
            news = search_news(query)
            if news:
                news_data[category] = news
                success = True
                break
            print(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(2)  # 添加延迟避免请求过快
    
    if success:
        save_news_json(news_data)
        print("Successfully saved news data")
    else:
        print("Failed to fetch any news")
        
if __name__ == "__main__":
    main()
