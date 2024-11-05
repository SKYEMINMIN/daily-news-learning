import requests
from datetime import datetime
import json

def get_news():
    # 使用免费的 News API
    try:
        url = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {
            'Ocp-Apim-Subscription-Key': 'YOUR_API_KEY'
        }
        response = requests.get(url, headers=headers)
        news = response.json()
        return news['value'][:5]  # 获取前5条新闻
    except Exception as e:
        return ["无法获取新闻: " + str(e)]

def update_html():
    news = get_news()
    
    # 读取原有的HTML内容
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # 更新新闻内容
    news_html = ""
    for item in news:
        news_html += f"<li>{item['name']}</li>\n"
    
    # 替换原有内容
    updated_html = html_content.replace('[Today\'s news will be here]', news_html)
    
    # 写入更新后的内容
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(updated_html)

if __name__ == "__main__":
    update_html()
