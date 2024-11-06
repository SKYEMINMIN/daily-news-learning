import json
import requests
from datetime import datetime
import logging
import sys
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_news.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def check_file_structure():
    """检查必要的文件结构"""
    required_paths = [
        'data',
        'css',
        'js',
        'scripts'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
            logging.error(f"Missing directory: {path}")
    
    return len(missing_paths) == 0

def check_api_access(api_key):
    """测试API访问"""
    test_url = f"https://newsapi.org/v2/everything?q=test&apiKey={api_key}"
    try:
        response = requests.get(test_url)
        if response.status_code == 200:
            logging.info("API access successful")
            return True
        else:
            logging.error(f"API access failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"API access error: {str(e)}")
        return False

def get_news():
    api_key = '70c47808e1fc40f2bb4450e822b5f2fc'
    news_data = {"ai": [], "entertainment": [], "finance": [], "politics": []}
    
    # 检查文件结构
    if not check_file_structure():
        logging.error("File structure check failed")
        return None
    
    # 检查API访问
    if not check_api_access(api_key):
        logging.error("API access check failed")
        return None
        
    urls = {
        "ai": f"https://newsapi.org/v2/everything?q=artificial+intelligence+OR+AI&language=en&sortBy=publishedAt&apiKey={api_key}",
        "entertainment": f"https://newsapi.org/v2/top-headlines?category=entertainment&language=en&apiKey={api_key}",
        "finance": f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}",
        "politics": f"https://newsapi.org/v2/top-headlines?category=politics&language=en&apiKey={api_key}"
    }
    
    for category, url in urls.items():
        try:
            logging.info(f"Fetching news for category: {category}")
            response = requests.get(url)
            
            if response.status_code != 200:
                logging.error(f"Failed to fetch {category} news. Status code: {response.status_code}")
                continue
                
            articles = response.json().get('articles', [])
            logging.info(f"Found {len(articles)} articles for {category}")
            
            for i, article in enumerate(articles[:2]):
                if article.get('title') and article.get('content'):
                    article_id = f"{category}-{datetime.now().strftime('%Y%m%d')}-{i+1}"
                    
                    news_item = {
                        "id": article_id,
                        "title": article['title'],
                        "link": article['url'],
                        "content": article['content'],
                        "category": category,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    news_data[category].append(news_item)
                    logging.info(f"Added article: {article_id}")
                    
        except Exception as e:
            logging.error(f"Error in category {category}: {str(e)}")
            continue
    
    return news_data

def save_news_data(news_data):
    """保存新闻数据并进行验证"""
    if news_data is None:
        logging.error("No news data to save")
        return False
        
    try:
        # 确保data目录存在
        Path('data').mkdir(exist_ok=True)
        
        # 保存数据
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
            
        # 验证保存的数据
        with open('data/news.json', 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            
        if saved_data == news_data:
            logging.info("News data saved and verified successfully")
            return True
        else:
            logging.error("Data verification failed after saving")
            return False
            
    except Exception as e:
        logging.error(f"Error saving news data: {str(e)}")
        return False

def main():
    logging.info("Starting news update process")
    
    try:
        news_data = get_news()
        if news_data and save_news_data(news_data):
            logging.info("News update completed successfully")
            return True
        else:
            logging.error("News update failed")
            return False
            
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
