import requests
import json
from datetime import datetime
import os
from pathlib import Path

def fetch_news():
    """获取新闻数据"""
    api_key = "70c47808e1fc40f2bb4450e822b5f2fc"
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        "apiKey": api_key,
        "country": "us",
        "pageSize": 5,
        "language": "en"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def create_markdown_content(article):
    """将单个新闻文章转换为Markdown格式"""
    title = article.get('title', '').replace('"', '\\"')
    description = article.get('description', 'No description available')
    url = article.get('url', '')
    source = article.get('source', {}).get('name', 'Unknown Source')
    
    markdown_content = f"""## News: {title}

### Source
{source}

### Content
{description}

### Original Link
[Read More]({url})

### Vocabulary
- word1: definition
- word2: definition
(Please add relevant vocabulary)

### Reading Comprehension
1. Question 1?
   - [ ] Option A
   - [ ] Option B
   - [ ] Option C
   - [ ] Option D

2. Question 2?
   - [ ] Option A
   - [ ] Option B
   - [ ] Option C
   - [ ] Option D

### Discussion
What do you think about this news? Share your thoughts!

---
"""
    return markdown_content

def generate_post():
    """生成完整的博客文章"""
    news_data = fetch_news()
    if not news_data or news_data.get('status') != 'ok':
        print("Failed to fetch news")
        return
    
    # 创建_posts目录（如果不存在）
    posts_dir = Path('_posts')
    posts_dir.mkdir(exist_ok=True)
    
    # 生成当前日期的文件名
    today = datetime.now()
    file_name = today.strftime('%Y-%m-%d-daily-news.md')
    file_path = posts_dir / file_name
    
    # 创建文章头部信息
    front_matter = f"""---
layout: post
title: "Daily News Learning {today.strftime('%Y-%m-%d')}"
date: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: daily-news
tags: [news, learning, english]
---

# Today's News Summary ({today.strftime('%Y-%m-%d')})

"""
    
    # 生成文章内容
    article_contents = []
    for article in news_data['articles']:
        if article['title'] != '[Removed]':
            article_contents.append(create_markdown_content(article))
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write('\n'.join(article_contents))
    
    print(f"Successfully generated post: {file_path}")

if __name__ == "__main__":
    generate_post()
