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
            "category": "general",  # 修改为 category
            "max": 10
        }
        
        print("Fetching news from Gnews API...")
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        
        # 打印响应内容以便调试
        print(f"Response content: {response.text[:500]}...")  # 只打印前500个字符
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查响应数据结构
            if 'errors' in data:
                raise Exception(f"API returned errors: {data['errors']}")
            
            formatted_data = {
                "status": "ok",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "articles": []
            }

            articles = data.get('articles', [])
            print(f"Found {len(articles)} articles in response")

            for article in articles:
                if _is_valid_article(article):
                    formatted_data["articles"].append(_format_article(article))

            print(f"Processed {len(formatted_data['articles'])} valid articles")
            return formatted_data
        else:
            error_message = f"API request failed with status {response.status_code}"
            try:
                error_detail = response.json()
                error_message += f": {json.dumps(error_detail)}"
            except:
                error_message += f": {response.text}"
            raise Exception(error_message)
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error in fetch_news: {str(e)}")
        raise

def _is_valid_article(article):
    """验证文章的有效性"""
    try:
        return all([
            article.get('title'),
            article.get('description'),
            article.get('url'),
            len(article.get('description', '')) > 50  # 降低长度要求
        ])
    except Exception as e:
        print(f"Error validating article: {str(e)}")
        return False

def _format_article(article):
    """格式化文章数据"""
    try:
        return {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", ""),
            "image": article.get("image", ""),
            "publishedAt": article.get("publishedAt", ""),
            "source": {
                "name": article.get("source", {}).get("name", "Unknown Source")
            }
        }
    except Exception as e:
        print(f"Error formatting article: {str(e)}")
        return None

def save_news(news_data):
    """保存新闻数据到JSON文件"""
    try:
        os.makedirs('data', exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f'data/news-{today}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"News data saved to {filename}")
        
        # 打印保存的数据摘要
        print(f"Saved {len(news_data.get('articles', []))} articles")
        
    except Exception as e:
        print(f"Error saving news data: {str(e)}")
        raise

def main():
    try:
        print("Starting news fetch process...")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        news_data = fetch_news()
        
        if news_data and news_data.get("articles"):
            print(f"Successfully retrieved {len(news_data['articles'])} articles")
            save_news(news_data)
            print("News update completed successfully!")
        else:
            raise Exception("No valid articles found in API response")
            
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
