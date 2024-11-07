import os
import json
import requests
from datetime import datetime, timezone

def fetch_news():
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            raise Exception("API key not found in environment variables")

        print(f"API Key (first 4 chars): {api_key[:4]}...")  # 仅打印前4个字符，安全起见

        # GNews API 配置
        url = "https://gnews.io/api/v4/search"
        params = {
            "token": api_key,
            "q": "world",
            "lang": "en",
            "max": 10,
            "in": "title,description"  # 在标题和描述中搜索
        }
        
        print("Fetching news from GNews API...")
        print(f"Request URL: {url}")
        # 打印参数时隐藏 token
        safe_params = params.copy()
        safe_params['token'] = '****'
        print(f"Using params: {safe_params}")
        
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"Response status: {response.status_code}")
        
        # 打印完整的响应内容用于调试
        print("Response content:")
        print(response.text)
        
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
        elif response.status_code == 403:
            raise Exception("API key authentication failed. Please check your API key.")
        elif response.status_code == 429:
            raise Exception("API rate limit exceeded. Please try again later.")
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
        has_required = all([
            article.get('title'),
            article.get('description'),
            article.get('url'),
            article.get('publishedAt')
        ])
        if not has_required:
            print(f"Article missing required fields: {article}")
            return False
        return True
    except Exception as e:
        print(f"Error validating article: {str(e)}")
        return False

def _format_article(article):
    """格式化文章数据，适配 GNews 的数据结构"""
    try:
        return {
            "title": article.get("title", "").strip(),
            "description": article.get("description", "").strip(),
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
        
        # 打印保存的文件大小和内容预览
        file_size = os.path.getsize(filename)
        print(f"Saved file size: {file_size} bytes")
        
        # 读取并打印保存的内容预览
        with open(filename, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            print(f"Saved {len(saved_data.get('articles', []))} articles")
            if saved_data.get('articles'):
                print("First article preview:")
                print(json.dumps(saved_data['articles'][C_0](), indent=2)[:200])
        
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
