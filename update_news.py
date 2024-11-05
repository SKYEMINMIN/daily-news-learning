import requests
from datetime import datetime
import json

def search_news():
    try:
        # 使用新闻 API
        url = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {
            'Ocp-Apim-Subscription-Key': 'your-api-key'
        }
        params = {
            'q': '重要新闻',
            'count': 5,
            'mkt': 'zh-CN'
        }
        
        # 如果没有 API key，我们就用备用方案
        news_list = [
            {"name": "今日要闻1", "url": "#"},
            {"name": "今日要闻2", "url": "#"},
            {"name": "今日要闻3", "url": "#"},
            {"name": "今日要闻4", "url": "#"},
            {"name": "今日要闻5", "url": "#"}
        ]
        return news_list
        
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return [{"name": "获取新闻失败，请稍后再试", "url": "#"}]

def update_html():
    news = search_news()
    
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        news_html = ""
        for item in news:
            news_html += f'<li><a href="{item["url"]}" target="_blank">{item["name"]}</a></li>\n'
        
        updated_html = html_content.replace('[Today\'s news will be here]', news_html)
        
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(updated_html)
        
        print("HTML updated successfully")
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")

if __name__ == "__main__":
    update_html()
