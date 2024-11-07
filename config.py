import os
import json
import requests
import pandas as pd
from datetime import datetime

def fetch_news():
    """获取新闻数据"""
    try:
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            raise ValueError("Missing NEWS_API_KEY environment variable")
        
        url = 'https://gnews.io/api/v4/top-headlines'
        params = {
            'apikey': api_key,
            'lang': 'zh',
            'country': 'cn',
            'max': 10
        }
        
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        if 'articles' not in data:
            return []
        
        articles = []
        for article in data['articles']:
            articles.append({
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'published': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', 'GNews')
            })
        
        return articles
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def save_files(articles):
    """保存所有文件格式"""
    try:
        # 保存 JSON
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        # 保存 CSV
        df = pd.DataFrame(articles)
        df.to_csv('news.csv', index=False, encoding='utf-8')

        # 生成 HTML
        html_content = """
        <html>
        <head>
            <meta charset="utf-8">
            <title>Daily News Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>每日新闻摘要</h1>
            <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        """
        
        df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">阅读全文</a>')
        df['published'] = pd.to_datetime(df['published']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df.columns = ['标题', '链接', '发布时间', '来源']
        
        html_content += df.to_html(index=False, escape=False)
        html_content += """
        </body>
        </html>
        """

        with open('news.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("Successfully saved all files")
        
    except Exception as e:
        print(f"Error saving files: {e}")
        print(f"Current working directory: {os.getcwd()}")
        raise

def main():
    print("Starting news fetch...")
    articles = fetch_news()
    print(f"Fetched {len(articles)} articles")
    
    if articles:
        save_files(articles)
        print("News data saved successfully")
    else:
        print("No articles to save")

if __name__ == "__main__":
    main()
