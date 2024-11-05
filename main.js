// 获取新闻数据的函数
async function getNews(category) {
    try {
        const response = await fetch(`data/${category.toLowerCase()}.json`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error loading ${category} news:`, error);
        return null;
    }
}

// 格式化时间的函数
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 更新时间显示
function updateDateTime() {
    const dateElement = document.getElementById('datetime');
    const now = new Date();
    dateElement.textContent = formatDate(now);
}

// 创建新闻卡片的HTML
function createNewsCard(news) {
    return `
        <div class="notion-news-item">
            <h3 class="notion-news-title">
                <a href="${news.url}" target="_blank" rel="noopener noreferrer">
                    ${news.title}
                </a>
            </h3>
            <div class="notion-news-meta">
                <span class="notion-news-source">${news.source || 'News Source'}</span>
                <span class="notion-news-time">${formatDate(news.time)}</span>
            </div>
        </div>
    `;
}

// 加载每个分类的新闻
async function loadCategoryNews() {
    const categories = ['AI', 'Entertainment', 'Finance', 'Politics'];
    
    for (const category of categories) {
        const newsContainer = document.getElementById(`${category.toLowerCase()}-news`);
        
        // 添加加载提示
        newsContainer.innerHTML = '<div class="notion-loading">Loading...</div>';
        
        try {
            const news = await getNews(category);
            if (news) {
                newsContainer.innerHTML = createNewsCard(news);
            } else {
                newsContainer.innerHTML = `
                    <div class="notion-error">
                        No news available for ${category}
                    </div>
                `;
            }
        } catch (error) {
            newsContainer.innerHTML = `
                <div class="notion-error">
                    Error loading ${category} news
                </div>
            `;
        }
    }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    updateDateTime();
    loadCategoryNews();
    
    // 每分钟更新一次时间
    setInterval(updateDateTime, 60000);
});
