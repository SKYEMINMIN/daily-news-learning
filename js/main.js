async function fetchNews() {
    try {
        const response = await fetch('data/news.json');
        const data = await response.json();
        displayNews(data);
    } catch (error) {
        console.error('Error fetching news:', error);
    }
}

function displayNews(data) {
    Object.keys(data).forEach(category => {
        const newsListElement = document.querySelector(`#${category} .news-list`);
        newsListElement.innerHTML = '';
        
        data[category].forEach(article => {
            const articleElement = document.createElement('div');
            articleElement.className = 'news-item';
            
            articleElement.innerHTML = `
                <h3>${article.title}</h3>
                <div class="news-links">
                    <a href="${article.link}" target="_blank">Original</a>
                    <a href="learning.html?id=${article.id}" class="learn-link">Learn</a>
                </div>
            `;
            
            newsListElement.appendChild(articleElement);
        });
    });
}

// 页面加载时获取新闻
document.addEventListener('DOMContentLoaded', fetchNews);
