import requests
import json
from datetime import datetime

def fetch_news():
    # 基本配置
    api_key = "70c47808e1fc40f2bb4450e822b5f2fc"
    base_url = "https://newsapi.org/v2/top-headlines"
    
    # 设置请求参数
    params = {
        "apiKey": api_key,
        "country": "us",
        "pageSize": 10,    # 获取更多新闻，因为有些可能被过滤掉
        "language": "en"
    }
    
    try:
        # 发送请求
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        news_data = response.json()
        
        if news_data["status"] == "ok":
            # 过滤掉已删除的文章
            valid_articles = [
                article for article in news_data["articles"]
                if article['title'] != '[Removed]' and article['description'] != '[Removed]'
            ]
            
            print(f"\n找到 {len(valid_articles)} 条有效新闻：\n")
            
            for i, article in enumerate(valid_articles[:5], 1):  # 只显示前5条有效新闻
                print(f"新闻 {i}:")
                print(f"标题: {article['title']}")
                
                # 转换时间格式
                try:
                    pub_time = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_time = pub_time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"发布时间: {formatted_time}")
                except:
                    print(f"发布时间: {article['publishedAt']}")
                
                print(f"描述: {article.get('description', '无描述')}")
                if article.get('url'):
                    print(f"链接: {article['url']}")
                print(f"来源: {article.get('source', {}).get('name', '未知来源')}")
                print("-" * 80 + "\n")
                
        else:
            print(f"获取新闻失败: {news_data.get('message', '未知错误')}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    print("开始获取最新新闻...")
    fetch_news()
