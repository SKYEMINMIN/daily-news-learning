import requests
import json
import os
from datetime import datetime
import pytz

# NewsAPI 配置
API_KEY = '70c47808e1fc40f2bb4450e822b5f2fc'
BASE_URL = 'https://newsapi.org/v2/everything'

def search_news(category):
    """
    使用 NewsAPI 获取特定类别的最新新闻
    """
    try:
        # 构建查询参数
        params = {
            'q': category,
            'apiKey': API_KEY,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 1  # 每个分类获取最新的一条新闻
        }
        
        # 发送请求
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # 检查请求是否成功
        
        data = response.json()
        
        if data['totalResults'] > 0:
            article = data['articles'][C_0]()  # 获取第一条新闻
            return {
                "title": article['title'],
                "url": article['url'],
                "source": article['source']['name'],
                "time": article['publishedAt']
            }
        else:
            print(f"No news found for category: {category}")
            return None
            
    except Exception as e:
        print(f"Error fetching {category} news: {e}")
        return None

def save_news_json(news_data):
    """
    将所有新闻保存到一个JSON文件
    """
    try:
        # 确保data目录存在
        os.makedirs('data', exist_ok=True)
        
        # 添加更新时间戳
        news_data['last_updated'] = datetime.now(pytz.UTC).isoformat()
        
        # 保存到news.json
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
            
        print("News data saved successfully")
    except Exception as e:
        print(f"Error saving news data: {e}")

def main():
    # 定义新闻类别和对应的搜索关键词
    categories = {
        'ai': 'artificial intelligence',
        'entertainment': 'entertainment news',
        'finance': 'financial news markets',
        'politics': 'political news'
    }
    
    # 收集所有新闻
    news_data = {}
    for category, search_term in categories.items():
        print(f"Fetching {category} news...")
        news = search_news(search_term)
        if news:
            news_data[category] = news
    
    # 保存新闻数据
    if news_data:
        save_news_json(news_data)
    else:
        print("No news data collected")

if __name__ == "__main__":
    main()
// 更新 formatDate 函数
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC',
        timeZoneName: 'short'
    }).format(date);
}

// 其余代码保持不变...
