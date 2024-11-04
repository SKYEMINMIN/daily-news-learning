---
layout: default
title: Daily News Learning
---

<div class="home-container">
    <section class="welcome-section">
        <h1>Welcome to Daily News Learning</h1>
        <p>Improve your English through daily news articles from trusted sources.</p>
    </section>

    <section class="latest-news">
        <h2>Latest Articles</h2>
        <div class="articles-grid">
            {% for post in site.posts limit:3 %}
            <article class="article-card">
                <span class="article-category">{{ post.category }}</span>
                <h3><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h3>
                <div class="article-meta">
                    <span class="article-date">{{ post.date | date: "%B %d, %Y" }}</span>
                    <span class="article-source">Source: {{ post.source }}</span>
                </div>
            </article>
            {% endfor %}
        </div>
    </section>

    <section class="features">
        <h2>Why Learn With Us?</h2>
        <div class="features-grid">
            <div class="feature-card">
                <h3>Daily Updates</h3>
                <p>New articles every day from reliable sources</p>
            </div>
            <div class="feature-card">
                <h3>Vocabulary Building</h3>
                <p>Key words and phrases explained in context</p>
            </div>
            <div class="feature-card">
                <h3>Discussion Questions</h3>
                <p>Practice critical thinking and expression</p>
            </div>
        </div>
    </section>
</div>
