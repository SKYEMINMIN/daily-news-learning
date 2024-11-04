---
layout: default
title: Home
---

# Welcome to Daily News Learning Hub

## Today's Featured Articles

{% for post in site.posts limit:3 %}
<div class="featured-article">
    <h3><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h3>
    <div class="article-meta">
        <span class="category">{{ post.category }}</span>
        <span class="source">Source: {{ post.source }}</span>
    </div>
</div>
{% endfor %}

## Why Learn with Daily News?

- **Real-world Context**: Learn English through current events
- **Vocabulary Building**: Learn new words in context
- **Reading Comprehension**: Improve your understanding
- **Discussion Practice**: Engage with thought-provoking questions

[Browse All Articles]({{ site.baseurl }}/news)
