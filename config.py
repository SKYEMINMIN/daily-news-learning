import os
import json
import requests
from datetime import datetime, timezone

def fetch_news():
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            raise Exception("API key not found in environment variables")

        # GNews API 配置
        url = "https://gnews.io/api/v4/search"
        params = {
            "token": api_key,  # GNews 使用 token 而不是 apiKey
            "q": "world",      # 搜索关键词
            "lang": "en",      # 英语新闻
            "max": 10          # 最大条数
        }
        
        print("Fetching news from GNews API...")
        print(f"Request URL: {url}")
        print(f"Using params: {params}")
        
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            
            formatted_data = {
                "status": "ok",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "totalArticles": data.get("totalArticles", 0),
                "articles": []
            }

            articles = data.get('articles', [])
            print(f"Found {len(articles)} articles in response")

            for article in articles:
                if _is_valid_article(article):
                    processed_article = _format_article(article)
                    if processed_article:
                        formatted_data["articles"].append(processed_article)

            print(f"Processed {len(formatted_data['articles'])} valid articles")
            
            if not formatted_data["articles"]:
                print("Warning: No valid articles found after processing")
                return None
                
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
            len(article.get('description', '')) > 50,
            article.get('publishedAt')
        ])
    except Exception as e:
        print(f"Error validating article: {str(e)}")
        return False

def _format_article(article):
    """格式化文章数据，适配 GNews 的数据结构"""
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
        
        # 打印保存的文件大小
        file_size = os.path.getsize(filename)
        print(f"Saved file size: {file_size} bytes")
        
    except Exception as e:
        print(f"Error saving news data: {str(e)}")
        raise

def main():
    try:
        print(f"Script started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working directory: {os.getcwd()}")
        
        news_data = fetch_news()
        
        if news_data and news_data.get("articles"):
            print(f"Successfully retrieved {len(news_data['articles'])} articles")
            save_news(news_data)
            print("News update completed successfully!")
        else:
            print("No valid news data to save")
            # 创建空的数据文件以避免工作流失败
            empty_data = {
                "status": "no_content",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "articles": []
            }
            save_news(empty_data)
            
    except Exception as e:
        print(f"Critical error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
