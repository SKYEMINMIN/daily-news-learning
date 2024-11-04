import requests
import json
from datetime import datetime

def fetch_news_by_category(category='general'):
    """
    获取指定类别的新闻
    类别选项: business, entertainment, general, health, science, sports, technology
    """
    api_key = "70c47808e1fc40f2bb4450e822b5f2fc"
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        "apiKey": api_key,
        "country": "us",
        "category": category,
        "pageSize": 10,
        "language": "en"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取新闻时出错: {e}")
        return None

def display_news_menu():
    categories = [
        'general', 'business', 'technology', 'entertainment',
        'sports', 'science', 'health'
    ]
    
    while True:
        print("\n=== 新闻类别选择 ===")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat.title()}")
        print("0. 退出")
        
        try:
            choice = int(input("\n请选择新闻类别 (0-7): "))
            if choice == 0:
                print("感谢使用！再见！")
                break
            elif 1 <= choice <= len(categories):
                category = categories[choice-1]
                print(f"\n正在获取 {category.title()} 类别的新闻...")
                news_data = fetch_news_by_category(category)
                
                if news_data and news_data["status"] == "ok":
                    valid_articles = [
                        article for article in news_data["articles"]
                        if article['title'] != '[Removed]' and article['description'] != '[Removed]'
                    ]
                    
                    print(f"\n找到 {len(valid_articles)} 条相关新闻：\n")
                    
                    for i, article in enumerate(valid_articles[:5], 1):
                        print(f"新闻 {i}:")
                        print(f"标题: {article['title']}")
                        print(f"来源: {article.get('source', {}).get('name', '未知来源')}")
                        print(f"描述: {article.get('description', '无描述')}")
                        print(f"链接: {article.get('url', '无链接')}")
                        print("-" * 80 + "\n")
                        
                input("按回车键继续...")
            else:
                print("无效的选择，请重试！")
        except ValueError:
            print("请输入有效的数字！")

if __name__ == "__main__":
    print("欢迎使用新闻浏览器！")
    display_news_menu()
