import os
import json
import requests
from datetime import datetime, timezone

def fetch_news():
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            raise Exception("API key not found in environment variables")

        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "token": api_key,
            "lang": "en",
            "country": "us",
            "max": 10,
            "topic": "world"  # 专注国际新闻
        }
        
        print("Fetching news from Gnews API...")
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            formatted_data = {
                "status": "ok",
                "articles": []
            }

            for article in data.get('articles', []):
                if _is_valid_article(article):
                    formatted_data["articles"].append(_format_article(article))

            if not formatted_data["articles"]:
                raise Exception("No valid articles found")

            return formatted_data
        else:
            print(f"Error response: {response.text}")
            raise Exception(f"API request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error in fetch_news: {str(e)}")
        raise

def _is_valid_article(article):
    """验证文章的有效性"""
    return all([
        article.get('title'),
        article.get('description'),
        article.get('url'),
        len(article.get('description', '')) > 100,
        not any(word in article['title'].lower() for word in ['removed', '[removed]'])
    ])

def _format_article(article):
    """格式化文章数据"""
    return {
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "urlToImage": article.get("image", ""),
        "publishedAt": article["publishedAt"],
        "source": {
            "name": article.get("source", {}).get("name", "Unknown Source")
        }
    }

def save_news(news_data):
    """保存新闻数据到JSON文件"""
    os.makedirs('data', exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/news-{today}.json'
    
    try:
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
        
        if news_data and news_data["articles"]:
            print(f"Retrieved {len(news_data['articles'])} valid articles")
            save_news(news_data)
            print("News update completed successfully!")
        else:
            raise Exception("No articles found in API response")
            
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
