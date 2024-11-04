---
layout: default
title: Home
---

# Welcome to Daily News Learning

Latest News Posts:

{% for post in site.posts limit:5 %}
* {{ post.date | date: "%Y-%m-%d" }} - [{{ post.title }}]({{ site.baseurl }}{{ post.url }})
{% endfor %}
