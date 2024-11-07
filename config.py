import os
import json
import requests
import pandas as pd
from datetime import datetime

def fetch_news():
    """获取新闻数据"""
    try:
        # 获取API密钥
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            raise ValueError("Missing NEWS_API_KEY environment variable")
        
        # API请求参数
        url = 'https://gnews.io/api/v4/top-headlines'
        params = {
            'apikey': api_key,
            'lang': 'zh',
            'country': 'cn',
            'max': 10
        }
        
        # 发送请求
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        if 'articles' not in data:
            return []
        
        # 处理文章数据
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

def generate_report(articles):
    """生成HTML报告"""
    if not articles:
        return "<p>No articles found</p>"
    
    # HTML头部
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
    
    # 创建数据表格
    df = pd.DataFrame(articles)
    df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">阅读全文</a>')
    df['published'] = pd.to_datetime(df['published']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df.columns = ['标题', '链接', '发布时间', '来源']
    
    # 添加表格到HTML
    html_content += df.to_html(index=False, escape=False)
    html_content += """
    </body>
    </html>
    """
    
    return html_content

def save_report(html_content):
    """保存HTML报告"""
    try:
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"news_report_{timestamp}.html"
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    except Exception as e:
        print(f"Error saving report: {e}")
        print(f"Working directory: {os.getcwd()}")
        raise

def main():
    # 获取新闻
    articles = fetch_news()
    
    # 生成报告
    html_report = generate_report(articles)
    
    # 保存报告
    filename = save_report(html_report)
    print(f"Report saved as: {filename}")

if __name__ == "__main__":
    main()
