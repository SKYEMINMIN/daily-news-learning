import json
import os
import sys
import logging
import requests
from datetime import datetime, timezone, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_news.log'),
        logging.StreamHandler()
    ]
)

def fetch_news():
    """从 NewsAPI 获取新闻"""
    try:
        # NewsAPI endpoint 和 API key
        url = "https://newsapi.org/v2/top-headlines"
        api_key = "8156377f05e547f587b7bb470cece80e"  # 这是你的 API key
        
        # 设置请求参数
        params = {
            "apiKey": api_key,
            "language": "en",
            "country": "us",
            "pageSize": 5  # 限制获取的新闻数量
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching news: {str(e)}")
        return None

def process_news(news_data):
    """处理新闻数据"""
    if not news_data or "articles" not in news_data:
        return []
        
    processed_news = []
    
    for article in news_data["articles"]:
        # 跳过没有内容的文章
        if not article.get("content"):
            continue
            
        # 生成唯一ID（使用时间戳和标题的组合）
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        title_part = article.get("title", "")[:30].replace(" ", "-").lower()
        article_id = f"{timestamp}-{title_part}"
        
        processed_article = {
            "id": article_id,
            "title": article.get("title", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "publishedAt": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "Unknown")
        }
        
        processed_news.append(processed_article)
    
    return processed_news

def save_news(news_list):
    """保存新闻到文件"""
    try:
        # 确保目录存在
        os.makedirs('data', exist_ok=True)
        
        # 读取现有的新闻（如果存在）
        existing_news = []
        if os.path.exists('data/news.json'):
            with open('data/news.json', 'r', encoding='utf-8') as f:
                existing_news = json.load(f)
        
        # 合并新旧新闻，保持最近的10条
        all_news = news_list + existing_news
        all_news = all_news[:10]  # 只保留最新的10条新闻
        
        # 保存到文件
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
            
        logging.info(f"Successfully saved {len(news_list)} new news items")
        return True
        
    except Exception as e:
        logging.error(f"Error saving news: {str(e)}")
        return False

def main():
    try:
        # 获取新闻
        news_data = fetch_news()
        if not news_data:
            logging.error("Failed to fetch news")
            return False
            
        # 处理新闻
        processed_news = process_news(news_data)
        if not processed_news:
            logging.error("No valid news to process")
            return False
            
        # 保存新闻
        success = save_news(processed_news)
        
        return success
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
