import requests
from datetime import datetime

def search_news():
    try:
        # 使用 search API 获取新闻
        response = requests.get('https://api.example.com/news')  # 替换为实际的新闻 API
        
        # 示例新闻数据
        news_list = [
            {"name": "今日要闻1", "url": "https://example.com/news1"},
            {"name": "今日要闻2", "url": "https://example.com/news2"},
            {"name": "今日要闻3", "url": "https://example.com/news3"},
            {"name": "今日要闻4", "url": "https://example.com/news4"},
            {"name": "今日要闻5", "url": "https://example.com/news5"}
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
