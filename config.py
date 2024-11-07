import os  
import requests  
import pandas as pd  
from datetime import datetime  

def fetch_news(api_key, lang, country, max_results):  
    """获取新闻数据"""  
    try:  
        url = 'https://gnews.io/api/v4/top-headlines'  
        params = {  
            'token': api_key,  
            'lang': lang,  
            'country': country,  
            'max': max_results  
        }  

        response = requests.get(url, params=params, timeout=30)  
        response.raise_for_status()  
        data = response.json()  

        articles = []  
        if 'articles' in data:  
            for article in data['articles']:  
                articles.append({  
                    'title': article.get('title', ''),  
                    'url': article.get('url', ''),  
                    'publishedAt': article.get('publishedAt', ''),  
                    'source': article.get('source', {}).get('name', 'Unknown')  
                })  
        return articles  
    except requests.exceptions.RequestException as e:  
        print(f"Error fetching news: {e}")  
        return []  
    except Exception as e:  
        print(f"Unexpected error fetching news: {e}")  
        return []

def main():  
    print("Starting news collection process...")  

    api_key = 'dc6b340bb21432e40ed552ac70befd79'  
    lang = 'zh'  
    country = 'cn'  
    max_results = 10  
    output_file = 'news.html'  

    # 获取新闻  
    articles = fetch_news(api_key, lang, country, max_results)  
    print(f"Retrieved {len(articles)} articles")  

    # 保存HTML  
    save_as_html(articles, output_file)  
    print("Process completed")  

if __name__ == "__main__":  
    main()
