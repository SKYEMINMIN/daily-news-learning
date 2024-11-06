import os
import json
import requests
import time
from datetime import datetime

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
            "max": 5  # 减少到5条新闻
        }
        
        print(f"Fetching news from Gnews API...")
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        print(f"Response content type: {response.headers.get('content-type', '')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Articles found: {len(data.get('articles', []))}")
                
                # 检查响应结构
                if 'articles' not in data:
                    print(f"Unexpected response structure: {data}")
                    raise Exception("Invalid API response format")

                formatted_data = {
                    "status": "ok",
                    "articles": []
                }

                for article in data['articles']:
                    try:
                        formatted_article = {
                            "title": article.get("title", "No title"),
                            "description": article.get("description", "No description"),
                            "url": article.get("url", ""),
                            "urlToImage": article.get("image", ""),
                            "publishedAt": article.get("publishedAt", ""),
                            "source": {
                                "name": article.get("source", {}).get("name", "Unknown Source")
                            }
                        }
                        formatted_data["articles"].append(formatted_article)
                    except Exception as e:
                        print(f"Error formatting article: {e}")
                        continue

                if not formatted_data["articles"]:
                    raise Exception("No articles could be processed")

                return formatted_data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
                raise
        else:
            error_message = f"API request failed with status {response.status_code}"
            try:
                error_details = response.json()
                error_message += f": {error_details}"
            except:
                error_message += f": {response.text}"
            print(error_message)
            raise Exception(error_message)
            
    except Exception as e:
        print(f"Error in fetch_news: {str(e)}")
        raise

def save_news(news_data):
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
        
        if news_data and news_data.get('articles'):
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
