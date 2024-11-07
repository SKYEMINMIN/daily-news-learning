import os
import json
import requests
import pandas as pd
from datetime import datetime
from json2html import json2html

def fetch_news():
    try:
        # GNews.io API配置
        api_key = os.getenv('NEWS_API_KEY', 'dc6b340bb21432e40ed552ac70befd79')
        url = 'https://gnews.io/api/v4/search'
        params = {
            'token': api_key,
            'lang': 'zh',
            'country': 'cn',
            'n': 10,  # 正确的参数名是 n，而不是 max
            'q': '热点',  # 使用中文关键词可能更合适
            'sortby': 'publishedAt'
        }
        
        # 发送请求获取数据
        response = requests.get(url, params=params, timeout=30)
        
        # 打印响应以便调试
        print(f"API Response Status: {response.status_code}")
        print(f"API Response: {response.text[:500]}")
        
        data = response.json()
        
        processed_articles = []
        if 'articles' in data:
            for article in data['articles']:
                processed_article = {
                    'title': article.get('title', ''),
                    'link': article.get('url', ''),
                    'published': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', 'GNews')
                }
                processed_articles.append(processed_article)
        
        return processed_articles
    
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        print(f"Full API response: {response.text if 'response' in locals() else 'No response'}")
        return []

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_to_html(data, filename):
    # 将JSON转换为HTML表格
    html_content = json2html.convert(json=data)
    
    # 添加HTML样式
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>每日新闻更新</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            a {{
                color: #2196F3;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>每日新闻更新</h1>
            <p>更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        {html_content}
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(styled_html)

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

def main():
    # 获取新闻数据
    news_data = fetch_news()
    
    if news_data:
        # 保存为不同格式
        save_to_json(news_data, 'news.json')
        save_to_html(news_data, 'news.html')
        save_to_csv(news_data, 'news.csv')
        print("News data has been successfully updated and saved.")
    else:
        print("No news data was retrieved.")

if __name__ == "__main__":
    main()
