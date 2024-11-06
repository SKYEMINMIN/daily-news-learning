import json
import requests
from datetime import datetime
from learning_processor import LearningMaterialGenerator

def get_news():
    api_key = '70c47808e1fc40f2bb4450e822b5f2fc'
    news_data = {"ai": [], "entertainment": [], "finance": [], "politics": []}
    learning_generator = LearningMaterialGenerator()
    
    urls = {
        "ai": f"https://newsapi.org/v2/everything?q=artificial+intelligence+OR+AI&language=en&sortBy=publishedAt&apiKey={api_key}",
        "entertainment": f"https://newsapi.org/v2/top-headlines?category=entertainment&language=en&apiKey={api_key}",
        "finance": f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}",
        "politics": f"https://newsapi.org/v2/top-headlines?category=politics&language=en&apiKey={api_key}"
    }
    
    for category, url in urls.items():
        try:
            response = requests.get(url)
            articles = response.json().get('articles', [])
            
            for i, article in enumerate(articles[:2]):
                if article.get('title') and article.get('content'):
                    article_id = f"{category}-{datetime.now().strftime('%Y%m%d')}-{i+1}"
                    
                    learning_materials = {
                        "paragraphs": learning_generator.process_text(article['content']),
                        "questions": learning_generator.generate_questions(article['content'])
                    }
                    
                    news_item = {
                        "id": article_id,
                        "title": article['title'],
                        "link": article['url'],
                        "content": article['content'],
                        "learning_materials": learning_materials
                    }
                    
                    news_data[category].append(news_item)
                    
        except Exception as e:
            print(f"Error in category {category}: {str(e)}")
            continue
    
    return news_data

def main():
    try:
        news_data = get_news()
        with open('data/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
        print("News updated successfully!")
    except Exception as e:
        print(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()
