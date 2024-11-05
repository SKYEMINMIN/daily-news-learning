import requests
import json
import os
from datetime import datetime
import pytz

# NewsAPI 配置
API_KEY = '70c47808e1fc40f2bb4450e822b5f2fc'
BASE_URL = 'https://newsapi.org/v2/everything'

def search_news(query):
    """
    使用 NewsAPI 获取新闻
    """
    try:
        headers = {
            'X-Api-Key': API_KEY,
            'User-Agent': 'Mozilla/5.0'
        }
        
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 1
        }
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'ok' and data['totalResults'] > 0:
            article = data['articles'][C_0]()
            return {
                "title": article['title'],
                "url": article['url'],
                "source": article['source']['name'],
                "time": article['publishedAt']
            }
        return None
            
    except Exception as e:
        print(f"Error fetching news for {query}: {e}")
        return None

def save_news_json(news_data):
    """
    保存新闻数据到JSON文件
    """
    try:
        # 确保data目录存在
        os.makedirs('data', exist_ok=True)
        
        # 创建输出数据结构
        output = {
            "metadata": {
                "last_updated": datetime.now(pytz.UTC).isoformat()
            },
            "news": news_data
        }
        
        # 保存到文件
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        print("News data saved successfully")
    except Exception as e:
        print(f"Error saving news data: {e}")

def main():
    # 定义新闻搜索关键词
    queries = {
        'ai': 'artificial intelligence technology',
        'entertainment': 'entertainment news',
        'finance': 'financial markets news',
        'politics': 'political news'
    }
    
    # 收集新闻
    news_data = {}
    for category, query in queries.items():
        print(f"Fetching {category} news...")
        news = search_news(query)
        if news:
            news_data[category] = news
    
    # 保存数据
    if news_data:
        save_news_json(news_data)
    else:
        print("No news data collected")

if __name__ == "__main__":
    main()
