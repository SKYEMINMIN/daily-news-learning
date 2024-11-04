from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests
from googletrans import Translator

def fetch_news():
    """获取新闻数据"""
    API_KEY = 'YOUR_NEWS_API_KEY'  # 替换为您的 API 密钥
    url = 
f'https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}'
    
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def generate_post():
    """生成博客文章"""
    news_data = fetch_news()
    
    if not news_data or news_data.get('status') != 'ok':
        print("Failed to fetch news")
        return
    
    posts_dir = Path('_posts')
    posts_dir.mkdir(exist_ok=True)
    
    tz = timezone(timedelta(hours=8))
    today = datetime.now(tz)
    file_name = today.strftime('%Y-%m-%d-daily-news.md')
    file_path = posts_dir / file_name

    content = create_post_content(news_data, today)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully generated post: {file_path}")

def create_post_content(news_data, today):
    """创建文章内容"""
    front_matter = f"""---
layout: post
title: "每日英语新闻学习 ({today.strftime('%Y-%m-%d')})"
date: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: daily-news
tags: [english-learning, news, vocabulary]
---

# Today's English News

_Date: {today.strftime('%B %d, %Y')} | Daily English Learning Through 
News_

"""
    
    article_contents = []
    for idx, article in enumerate(news_data['articles'][:5], 1):
        if article.get('title') and article['title'] != '[Removed]':
            article_contents.append(create_article_content(article, idx))
    
    return front_matter + '\n'.join(article_contents)

def create_article_content(article, index):
    """创建单篇文章的内容"""
    title = article.get('title', '').replace('"', '\\"')
    description = article.get('description', 'No description available')
    url = article.get('url', '')
    source = article.get('source', {}).get('name', 'Unknown Source')
    
    return f"""## News #{index}

<div class="news-card">

### 📰 {title}

**Source**: {source}  
**Link**: [Read Original Article]({url})

#### English Content
<div class="english-content">
{description}
</div>

#### Key Words & Phrases
<div class="vocabulary-section">
| Word/Phrase | Definition | Usage |
|------------|------------|--------|
| (key word 1) | (definition) | (example) |
| (key word 2) | (definition) | (example) |
</div>

#### Comprehension Check
<div class="comprehension-section">
1️⃣ **Main Idea**:
<details>
<summary>Click to see the main point</summary>
<div class="answer-box">
Main idea of the article
</div>
</details>

2️⃣ **Key Details**:
<details>
<summary>Click to see key points</summary>
<div class="answer-box">
- Point 1
- Point 2
- Point 3
</div>
</details>
</div>

#### Practice Section
<div class="practice-section">
🗣️ **Discussion Question**:  
What do you think about this news?

✍️ **Writing Prompt**:  
Write a brief summary of this news in your own words.
</div>

</div>

---
"""

if __name__ == "__main__":
    generate_post()

