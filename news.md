---
layout: default
title: News
---

<div class="news-page">
    <h1>Latest News</h1>
    
    <div class="category-filters">
        <button class="filter-btn active" data-category="all">All</button>
        <button class="filter-btn" data-category="AI">AI</button>
        <button class="filter-btn" data-category="News">News</button>
        <button class="filter-btn" data-category="Entertainment">Entertainment</button>
    </div>

    <div class="articles-grid">
        {% for post in site.posts %}
        <div class="article-card" data-category="{{ post.category }}">
            <span class="article-category">{{ post.category }}</span>
            <h2><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h2>
            <div class="article-meta">
                <span class="article-date">{{ post.date | date: "%B %d, %Y" }}</span>
                <span class="article-source">Source: {{ post.source }}</span>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
