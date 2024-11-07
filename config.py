import os
import ssl
import json
import requests
import urllib3
import pandas as pd
from datetime import datetime
from json2html import json2html

# SSL验证配置
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

# 获取API密钥
API_KEY = os.environ.get('GNEWS_API_KEY')

def fetch_news():
    # GNews API配置
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        'token': API_KEY,
        'lang': 'zh',  # 中文新闻
        'country': 'cn',  # 中国新闻
        'max': 10  # 获取10条新闻
    }

    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  # 检查请求是否成功
        news_data = response.json()
        
        # 提取所需的新闻信息
        articles = news_data.get('articles', [])
        processed_articles = []
        
        for article in articles:
            processed_article = {
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'publishedAt': article.get('publishedAt'),
                'source': article.get('source', {}).get('name')
            }
            processed_articles.append(processed_article)
        
        return processed_articles
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
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
