import json
import requests
import translators as ts
from datetime import datetime

def get_news():
    api_key = '70c47808e1fc40f2bb4450e822b5f2fc'
    news_data = {"ai": [], "entertainment": [], "finance": [], "politics": []}
    
    # 定义新闻分类和对应的API URL
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
            
            for article in articles[:2]:  # 每类取2条最新新闻
                if article['title'] and article['description']:  # 确保标题和描述不为空
                    try:
                        # 使用Google翻译服务
                        chinese_content = ts.google(article['description'], from_language='en', to_language='zh')
                        
                        news_item = {
                            "title": article['title'],
                            "link": article['url'],
                            "content": article['description'],
                            "chinese": chinese_content
                        }
                        news_data[category].append(news_item)
                    except Exception as e:
                        print(f"Translation error: {e}")
                        continue
                        
            if len(news_data[category]) < 1:  # 如果该分类下没有新闻
                news_data[category].append({
                    "title": f"No {category} news available",
                    "link": "",
                    "content": "Currently no news available in this category",
                    "chinese": "当前分类暂无新闻"
                })
                
        except Exception as e:
            print(f"Error fetching {category} news: {e}")
            continue
    
    return news_data

def main():
    try:
        news_data = get_news()
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
        print("News updated successfully!")
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
