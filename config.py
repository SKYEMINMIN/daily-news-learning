import os
import json
import requests
import pandas as pd
from datetime import datetime
from json2html import json2html

def fetch_news():
    try:
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            raise ValueError("Missing NEWS_API_KEY environment variable")
            
        url = 'https://gnews.io/api/v4/top-headlines'
        params = {
            'apikey': api_key,  # 使用正确的参数名
            'lang': 'zh',
            'country': 'cn',
            'max': 10
        }

        
        print(f"Making request to GNews API...")
        response = requests.get(url, params=params, timeout=30)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # 检查响应是否是 JSON 格式
        try:
            data = response.json()
            print(f"Response data keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON. Response text: {response.text[:500]}")
            return []

        if 'errors' in data:
            print(f"API returned errors: {data['errors']}")
            return []
            
        if 'articles' not in data:
            print(f"No articles found in response. Response data: {data}")
            return []
            
        processed_articles = []
        for article in data['articles']:
            processed_article = {
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'published': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', 'GNews')
            }
            processed_articles.append(processed_article)
        
        if not processed_articles:
            print("No articles were processed")
        else:
            print(f"Successfully processed {len(processed_articles)} articles")
            
        return processed_articles
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if 'response' in locals():
            print(f"Error response: {response.text[:500]}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if 'response' in locals():
            print(f"Error response: {response.text[:500]}")
        return []

# 其余代码保持不变...
