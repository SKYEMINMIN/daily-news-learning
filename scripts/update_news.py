import requests
import json
import os
import logging
from datetime import datetime
from bs4 import BeautifulSoup

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_news.log'),
        logging.StreamHandler()
    ]
)

def fetch_reuters_news():
    try:
        # Reuters RSS feeds
        rss_urls = {
            'Technology': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
            'Business': 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best',
            'Politics': 'https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best'
        }

        news_data = []
        
        for category, url in rss_urls.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item', limit=3)  # 每个分类获取3条新闻
                    
                    for item in items:
                        news_id = f"news_{len(news_data)}_{datetime.now().strftime('%Y%m%d')}"
                        content = item.find('description').text if item.find('description') else ''
                        
                        news_item = {
                            'id': news_id,
                            'category': category,
                            'title': item.find('title').text if item.find('title') else '',
                            'url': item.find('link').text if item.find('link') else '',
                            'content': content
                        }
                        news_data.append(news_item)
                        logging.info(f"Added news item: {news_item['title']}")
                
            except Exception as e:
                logging.error(f"Error fetching {category} news: {str(e)}")
                continue

        return news_data

    except Exception as e:
        logging.error(f"Error in fetch_reuters_news: {str(e)}")
        return []

def save_news(news_data):
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        logging.info(f"Successfully saved {len(news_data)} news items")
        return True
    except Exception as e:
        logging.error(f"Error saving news: {str(e)}")
        return False

def main():
    logging.info("Starting news update process")
    
    # 获取新闻
    news_data = fetch_reuters_news()
    
    if not news_data:
        logging.error("No news data fetched")
        return False
    
    # 保存新闻
    if not save_news(news_data):
        logging.error("Failed to save news data")
        return False
    
    logging.info("News update completed successfully")
    return True

if __name__ == "__main__":
    main()
