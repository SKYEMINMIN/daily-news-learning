import json
import os
import sys
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_demo_news():
    """生成演示新闻数据"""
    current_date = datetime.now().strftime('%Y%m%d')
    return [
        {
            "id": f"demo_1_{current_date}",
            "category": "Technology",
            "title": "Demo Technology Article",
            "url": "https://example.com/tech",
            "content": "This is a demonstration technology article.\n\nIt contains multiple paragraphs for testing purposes."
        },
        {
            "id": f"demo_2_{current_date}",
            "category": "Business",
            "title": "Demo Business Article",
            "url": "https://example.com/business",
            "content": "This is a demonstration business article.\n\nIt shows how the content structure works."
        }
    ]

def ensure_directories():
    """确保必要的目录存在"""
    try:
        logging.info("Creating necessary directories...")
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/study', exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Error creating directories: {str(e)}")
        return False

def save_news(news_data):
    """保存新闻数据"""
    try:
        logging.info("Attempting to save news data...")
        
        # 确保目录存在
        if not ensure_directories():
            return False
            
        file_path = 'data/news.json'
        logging.info(f"Saving to {file_path}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
            
        logging.info(f"Successfully saved {len(news_data)} news items")
        
        # 验证保存的文件
        if os.path.exists(file_path):
            logging.info(f"File size: {os.path.getsize(file_path)} bytes")
        
        return True
    except Exception as e:
        logging.error(f"Error saving news: {str(e)}")
        return False

def main():
    try:
        logging.info("Starting news update process...")
        
        # 生成演示新闻
        logging.info("Generating demo news...")
        news_data = get_demo_news()
        
        # 保存新闻
        if save_news(news_data):
            logging.info("News update completed successfully")
            
            # 显示文件内容作为调试信息
            try:
                with open('data/news.json', 'r', encoding='utf-8') as f:
                    logging.info("Contents of news.json:")
                    logging.info(f.read())
            except Exception as e:
                logging.error(f"Error reading saved file: {str(e)}")
                
            return True
        else:
            logging.error("Failed to save news data")
            return False
            
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        logging.exception("Detailed error information:")
        return False

if __name__ == "__main__":
    logging.info("Script started")
    success = main()
    logging.info(f"Script completed with success={success}")
    sys.exit(0 if success else 1)
