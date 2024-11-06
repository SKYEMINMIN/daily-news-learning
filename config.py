import os
import json
import requests
from datetime import datetime

def fetch_news():
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        raise Exception("NEWS_API_KEY not found in environment variables")
    
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",  # 可以改为其他国家代码
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"API Response Status Code: {response.status_code}")  # 添加调试信息
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error Response: {response.text}")  # 添加错误响应内容
            raise Exception(f"API request failed with status {response.status_code}")
    except Exception as e:
        print(f"Error in fetch_news: {str(e)}")
        raise

def save_news(news_data):
    # 确保 data 目录存在
    os.makedirs('data', exist_ok=True)
    
    # 生成带日期的文件名
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/news-{today}.json'
    
    try:
        # 保存新闻数据
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
