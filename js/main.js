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
    if (dateElement) {
        dateElement.textContent = formatDate(new Date());
    }
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
async function loadAllNews() {
    try {
        console.log('Loading news data...');
        const response = await fetch('data/news.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('News data loaded:', data);
        return data;
    } catch (error) {
        console.error('Error loading news:', error);
        return null;
    }
}

// 初始化页面
async function initializePage() {
    console.log('Initializing page...');
    updateDateTime();
    
    const newsData = await loadAllNews();
    if (!newsData) {
        console.error('Failed to load news data');
        return;
    }
    
    const categories = ['ai', 'entertainment', 'finance', 'politics'];
    
    categories.forEach(category => {
        const container = document.getElementById(`${category}-news`);
        if (!container) {
            console.error(`Container for ${category} not found`);
            return;
        }
        
        const news = newsData[category];
        container.innerHTML = news ? createNewsCard(news) : 
            '<div class="notion-error">No news available</div>';
    });
}

// 当页面加载完成时初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded');
    initializePage();
    // 每分钟更新时间
    setInterval(updateDateTime, 60000);
});
