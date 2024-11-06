import json
import os
import sys
import logging
import requests
from datetime import datetime, timezone

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


class NewsProcessor:
    def fetch_news(self):
        """从 NewsAPI 获取新闻"""
        try:
            url = "https://newsapi.org/v2/top-headlines"
            api_key = "70c47808e1fc40f2bb4450e822b5f2fc"
            
            params = {
                "apiKey": api_key,
                "language": "en",
                "country": "us",
                "pageSize": 5
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching news: {str(e)}")
            return None

    def process_news_data(self, news_data):
        """处理新闻数据"""
        if not news_data or "articles" not in news_data:
            return []
            
        processed_news = []
        
        for article in news_data["articles"]:
            if not article.get("content"):
                continue
                
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
            
            # 直接处理学习材料
            study_content = self.process_for_study(processed_article)
            if study_content:
                self.save_study_content(article_id, study_content)
            
            processed_news.append(processed_article)
        
        return processed_news

    def save_news(self, news_list):
        """保存新闻到文件"""
        try:
            os.makedirs('data', exist_ok=True)
            
            existing_news = []
            if os.path.exists('data/news.json'):
                with open('data/news.json', 'r', encoding='utf-8') as f:
                    existing_news = json.load(f)
            
            all_news = news_list + existing_news
            all_news = all_news[:10]  # 保留最新的10条
            
            with open('data/news.json', 'w', encoding='utf-8') as f:
                json.dump(all_news, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            logging.error(f"Error saving news: {str(e)}")
            return False

    def get_words(self, text):
        """提取单词"""
        try:
            for char in '.,?!-:;"\'()[]{}@#$%^&*+=<>~/\\':
                text = text.replace(char, ' ')
            words = [word.strip().lower() for word in text.split() 
                    if len(word.strip()) > 3 
                    and word.strip().isalnum()]
            return list(set(words))
        except Exception as e:
            logging.error(f"Word extraction error: {str(e)}")
            return []

    def process_for_study(self, news_item):
        """处理学习材料"""
        try:
            content = news_item.get('content', '')
            if not content:
                return None

            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()][:1]
            processed_paragraphs = []
            
            for para in paragraphs:
                if len(para) > 10:
                    words = self.get_words(para)
                    vocab_list = [{'word': word, 'translation': '请自行翻译'} 
                                for word in words[:3]]
                    
                    # 生成填空题
                    questions = []
                    if words:
                        word_to_blank = words[C_0]()
                        blank_sent = para.lower().replace(word_to_blank, '_____', 1)
                        questions.append({
                            'type': 'fill-in',
                            'question': blank_sent,
                            'answer': word_to_blank
                        })

                    processed_para = {
                        'english': para,
                        'chinese': '请自行翻译',
                        'vocabulary': vocab_list,
                        'questions': questions
                    }
                    processed_paragraphs.append(processed_para)
            
            return {
                'id': news_item.get('id', ''),
                'title': news_item.get('title', ''),
                'paragraphs': processed_paragraphs
            }
        except Exception as e:
            logging.error(f"Error processing study content: {str(e)}")
            return None

    def save_study_content(self, news_id, content):
        """保存学习材料"""
        try:
            if content is None:
                return
                
            os.makedirs('data/study', exist_ok=True)
            file_path = f'data/study/{news_id}.json'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Saved study content for {news_id}")
            
        except Exception as e:
            logging.error(f"Error saving study content: {str(e)}")

def main():
    try:
        processor = NewsProcessor()
        
        # 获取新闻
        news_data = processor.fetch_news()
        if not news_data:
            logging.error("Failed to fetch news")
            return False
            
        # 处理新闻
        processed_news = processor.process_news_data(news_data)
        if not processed_news:
            logging.error("No valid news to process")
            return False
            
        # 保存新闻
        success = processor.save_news(processed_news)
        
        return success
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
