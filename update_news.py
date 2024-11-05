import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

def search_news():
    try:
        # 使用我们的搜索函数获取新闻
        url = "https://news.baidu.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('div.hotnews a')[:5]  # 获取前5条新闻
        
        news_list = []
        for item in news_items:
            news_list.append({
                'name': item.text.strip(),
                'url': item.get('href', '#')
            })
        return news_list
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return [{"name": "获取新闻失败，请稍后再试", "url": "#"}]

def update_html():
    news = search_news()
    
    try:
        # 读取原有的HTML内容
        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # 更新新闻内容
        news_html = ""
        for item in news:
            news_html += f'<li><a href="{item["url"]}" target="_blank">{item["name"]}</a></li>\n'
        
        # 替换原有内容
        updated_html = html_content.replace('[Today\'s news will be here]', news_html)
        
        # 写入更新后的内容
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(updated_html)
        
        print("HTML updated successfully")
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")

if __name__ == "__main__":
    update_html()
