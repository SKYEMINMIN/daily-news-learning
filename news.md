---
layout: default
title: News
---

<div class="news-container">
    <h1>Latest News Articles</h1>
    
    <div class="category-filters">
        <button class="filter-btn active" data-category="all">All Categories</button>
        <button class="filter-btn" data-category="AI">AI</button>
        <button class="filter-btn" data-category="News">News</button>
        <button class="filter-btn" data-category="Entertainment">Entertainment</button>
    </div>

    <div class="articles-list">
        {% for post in site.posts %}
        <div class="article-card" data-category="{{ post.category }}">
            <div class="article-meta">
                <span class="article-date">{{ post.date | date: "%B %d, %Y" }}</span>
                <span class="article-category">{{ post.category }}</span>
            </div>
            <h2 class="article-title">
                <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
            </h2>
            <div class="article-source">
                Source: <a href="{{ post.source_url }}" target="_blank">{{ post.source }}</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
