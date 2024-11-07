import os
import json
import requests
import pandas as pd
from datetime import datetime

def fetch_news():
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
            print("No articles found in response")
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
            
        return processed_articles
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def generate_report(articles):
    """Generate HTML report from articles"""
    if not articles:
        return "<p>No articles found</p>"
    
    html_content = """
    <html>
    <head>
        <title>Daily News Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>每日新闻摘要</h1>
        <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    """
    
    df = pd.DataFrame(articles)
    df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">阅读全文</a>')
    df['published'] = pd.to_datetime(df['published']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df.columns = ['标题', '链接', '发布时间', '来源']
    
    html_content += df.to_html(index=False, escape=False)
    html_content += """
    </body>
    </html>
    """
    
    return html_content

def save_report(html_content):
    """Save the HTML report to a file"""
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"news_report_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    articles = fetch_news()
    html_report = generate_report(articles)
    filename = save_report(html_report)
    print(f"Report saved as: {filename}")

if __name__ == "__main__":
    main()
