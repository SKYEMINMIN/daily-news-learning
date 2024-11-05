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
    dateElement.textContent = formatDate(new Date());
}

// 创建新闻卡片的HTML
function createNewsCard(news) {
    if (!news) return '<div class="notion-error">News data not available</div>';
    
    return `
        <div class="notion-news-item">
            <h3 class="notion-news-title">
                <a href="${news.url}" target="_blank" rel="noopener noreferrer">
                    ${news.title}
                </a>
            </h3>
            <div class="notion-news-meta">
                <span class="notion-news-source">${news.source}</span> • 
                <span class="notion-news-time">${formatDate(news.time)}</span>
            </div>
        </div>
    `;
}

// 加载新闻数据
async function loadNews(category) {
    try {
        console.log(`Loading ${category} news...`);
        const response = await fetch(`data/${category.toLowerCase()}.json`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log(`${category} news loaded:`, data);
        return data;
    } catch (error) {
        console.error(`Error loading ${category} news:`, error);
        return null;
    }
}

// 初始化页面
async function initializePage() {
    console.log('Initializing page...');
    updateDateTime();
    
    const categories = ['ai', 'entertainment', 'finance', 'politics'];
    
    for (const category of categories) {
        const container = document.getElementById(`${category}-news`);
        if (!container) {
            console.error(`Container for ${category} not found`);
            continue;
        }
        
        container.innerHTML = '<div class="notion-loading">Loading...</div>';
        
        const news = await loadNews(category);
        container.innerHTML = news ? createNewsCard(news) : 
            '<div class="notion-error">Failed to load news</div>';
    }
}

// 当页面加载完成时初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded');
    initializePage();
    // 每分钟更新时间
    setInterval(updateDateTime, 60000);
});
