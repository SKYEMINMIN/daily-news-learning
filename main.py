import requests
from datetime import datetime

def search_news():
    try:
        keywords = "今日新闻 要闻"
        response = requests.get(
            'https://api.bing.com/v7.0/news/search',
            headers={
                'Ocp-Apim-Subscription-Key': 'your_api_key'
            },
            params={
                'q': keywords,
                'mkt': 'zh-CN',
                'count': 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            news_list = []
            for item in data.get('value', [])[:5]:
                news_list.append({
                    'name': item['name'],
                    'url': item['url']
                })
            return news_list
        else:
            return [{"name": f"获取新闻失败: {response.status_code}", "url": "#"}]
            
    except Exception as e:
        print(f"Error in search_news: {str(e)}")
        return [{"name": "获取新闻失败，请稍后再试", "url": "#"}]

def update_html():
    news = search_news()
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        news_html = "\n".join([f'<li><a href="{item["url"]}" target="_blank">{item["name"]}</a></li>' for item in news])
        
        updated_html = html_content.replace('[Today\'s news will be here]', news_html)
        
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(updated_html)
        
        print("HTML updated successfully!")
        print("Updated news items:")
        for item in news:
            print(f"- {item['name']}")
            
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")

if __name__ == "__main__":
    update_html()
