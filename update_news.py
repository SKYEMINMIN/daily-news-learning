import requests
from datetime import datetime

def search_news():
    try:
        # 使用搜索功能获取新闻
        search_term = "重要新闻 科技 时事"
        response = requests.get(f"https://api.bing.com/v7.0/news/search?q={search_term}&mkt=zh-CN")
        return response.json()['value'][:5]  # 获取前5条新闻
    except Exception as e:
        return [{"name": f"获取新闻失败: {str(e)}"}]

def update_html():
    news = search_news()
    
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
