import os  
import requests  
import pandas as pd  
from datetime import datetime  

def fetch_news():  
    """获取新闻数据"""  
    try:  
        api_key = 'dc6b340bb21432e40ed552ac70befd79'  
        
        url = 'https://gnews.io/api/v4/top-headlines'  
        params = {  
            'token': api_key,  
            'lang': 'zh',  
            'country': 'cn',  
            'max': 10  
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
    
    except Exception as e:  
        print(f"Error fetching news: {e}")  
        return []

def save_as_html(articles):  
    """保存为HTML文件"""  
    try:  
        # 创建DataFrame  
        df = pd.DataFrame(articles)  
        
        # 如果DataFrame为空，添加列名  
        if df.empty:  
            df = pd.DataFrame(columns=['title', 'url', 'publishedAt', 'source'])  
        
        # 格式化数据  
        df['url'] = df['url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>' if x else '')  
        df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.strftime('%Y-%m-%d %H:%M:%S')  
        
        # 重命名列  
        df.columns = ['Title', 'Link', 'Published', 'Source']  
        
        # 生成HTML  
        html_content = f"""  
        <!DOCTYPE html>  
        <html>  
        <head>  
            <meta charset="utf-8">  
            <title>News Report</title>  
            <style>  
                body {{ font-family: Arial, sans-serif; padding: 20px; }}  
                table {{ border-collapse: collapse; width: 100%; }}  
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}  
                th {{ background-color: #f2f2f2; }}  
            </style>  
        </head>  
        <body>  
            <h1>Daily News Report</h1>  
            <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>  
            {df.to_html(index=False, escape=False)}  
        </body>  
        </html>  
        """  
        
        # 保存文件  
        with open('news.html', 'w', encoding='utf-8') as f:  
            f.write(html_content)  
        
        print("HTML file saved successfully")  
        
    except Exception as e:  
        print(f"Error saving HTML: {e}")  
        raise  

def main():  
    print("Starting news collection process...")  
    
    # 获取新闻  
    articles = fetch_news()  
    print(f"Retrieved {len(articles)} articles")  
    
    # 保存HTML  
    save_as_html(articles)  
    print("Process completed")  

if __name__ == "__main__":  
    main()
