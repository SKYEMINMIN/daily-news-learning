// main.js
class NewsManager {
    constructor() {
        this.categories = ['ai', 'entertainment', 'finance', 'politics'];
        this.updateDateTime();
    }

    updateDateTime() {
        const datetimeElement = document.getElementById('datetime');
        if (datetimeElement) {
            datetimeElement.textContent = new Date().toLocaleString();
        }
    }

    async fetchNews() {
        try {
            const response = await fetch('data/news.json');
            if (!response.ok) {
                throw new Error('Failed to fetch news data');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching news:', error);
            return null;
        }
    }

    createNewsItem(item, category) {
        const newsElement = document.createElement('div');
        newsElement.className = 'notion-news-item';
        
        // 生成唯一的新闻ID
        const newsId = `${category}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        newsElement.innerHTML = `
            <div class="notion-news-content">
                <a href="${item.link}" 
                   target="_blank" 
                   class="notion-link"
                   title="${item.title}">
                    ${item.title}
                </a>
                <a href="study.html?id=${newsId}&category=${category}&title=${encodeURIComponent(item.title)}&link=${encodeURIComponent(item.link)}" 
                   class="notion-study-button">
                    Study
                </a>
            </div>
        `;
        
        return newsElement;
    }

    displayNewsInCategory(newsData, category) {
        const containerElement = document.getElementById(`${category}-news`);
        if (!containerElement || !newsData[category]) return;

        containerElement.innerHTML = ''; // Clear existing content
        
        newsData[category].forEach(item => {
            const newsElement = this.createNewsItem(item, category);
            containerElement.appendChild(newsElement);
        });
    }

    async displayAllNews() {
        const newsData = await this.fetchNews();
        if (!newsData) {
            this.handleError('Failed to load news');
            return;
        }

        this.categories.forEach(category => {
            this.displayNewsInCategory(newsData, category);
        });
    }

    handleError(message) {
        this.categories.forEach(category => {
            const container = document.getElementById(`${category}-news`);
            if (container) {
                container.innerHTML = `
                    <div class="notion-error">
                        <p>${message}</p>
                        <button onclick="newsManager.retryLoad()">Retry</button>
                    </div>
                `;
            }
        });
    }

    async retryLoad() {
        await this.displayAllNews();
    }

    init() {
        this.displayAllNews();
        // 每5分钟更新一次
        setInterval(() => {
            this.updateDateTime();
            this.displayAllNews();
        }, 300000);
    }
}

// 创建全局实例
const newsManager = new NewsManager();

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    newsManager.init();
});
