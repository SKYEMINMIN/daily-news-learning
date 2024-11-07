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
        
        print(f"Making request to GNews API...")
        response = requests.get(url, params=params, timeout=30)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
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

def generate_report(articles):
    """Generate HTML report from articles"""
    if not articles:
        return "<p>No articles found</p>"
    
    # 创建HTML表格头部
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
            .title { font-weight: bold; }
            .date { color: #666; }
        </style>
    </head>
    <body>
        <h1>每日新闻摘要</h1>
        <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    """
    
    # 转换为DataFrame并生成HTML表格
    df = pd.DataFrame(articles)
    # 将链接转换为可点击的HTML链接
    df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">阅读全文</a>')
    # 格式化发布时间
    df['published'] = pd.to_datetime(df['published']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 重命名列
    df.columns = ['标题', '链接', '发布时间', '来源']
    
    html_content += df.to_html(index=False, escape=False)
    html_content += """
    </body>
    </html>
    """
    
    return html_content

def save_report(html_content):
    """Save the HTML report to a file"""
    try:
        # 使用相对于工作目录的路径
        reports_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        print(f"Created/verified reports directory at: {reports_dir}")
        
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = os.path.join(reports_dir, f"news_report_{timestamp}.html")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report saved as {filename}")
        return filename
    except PermissionError as e:
        print(f"Permission error while creating directory or file: {e}")
        # 如果创建目录失败，尝试直接在当前目录保存
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"news_report_{timestamp}.html"
        print(f"Attempting to save in current directory: {os.getcwd()}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved report in current directory: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving report: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir('.')}")
        raise

def main():
    articles = fetch_news()
    html_report = generate_report(articles)
    filename = save_report(html_report)
    print(f"Report generation completed. File saved as: {filename}")

if __name__ == "__main__":
    main()
