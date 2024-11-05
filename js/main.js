document.addEventListener('DOMContentLoaded', () => {
    // 更新日期时间显示
    updateDateTime();
    // 加载新闻数据
    loadNews();
});

// 更新日期时间
function updateDateTime() {
    const datetimeElement = document.getElementById('datetime');
    if (datetimeElement) {
        datetimeElement.textContent = new Date().toLocaleString();
    }
    // 每分钟更新一次时间
    setInterval(updateDateTime, 60000);
}

// 加载新闻数据
async function loadNews() {
    try {
        const response = await fetch('data/news.json');
        const data = await response.json();
        
        // 处理每个分类的新闻
        Object.keys(data).forEach(category => {
            displayCategoryNews(category, data[category]);
        });
    } catch (error) {
        console.error('Error loading news:', error);
        handleError();
    }
}

// 显示分类新闻
function displayCategoryNews(category, news) {
    const container = document.getElementById(`${category}-news`);
    if (!container) return;

    // 清空现有内容
    container.innerHTML = '';

    // 添加新闻项
    news.forEach(item => {
        const newsElement = createNewsElement(item, category);
        container.appendChild(newsElement);
    });
}

// 创建新闻元素
function createNewsElement(item, category) {
    const div = document.createElement('div');
    div.className = 'notion-news-item';

    const newsId = `${category}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    div.innerHTML = `
        <div class="notion-news-content">
            <a href="${item.link}" 
               target="_blank" 
               class="notion-link">
                ${item.title}
            </a>
            <a href="study.html?id=${newsId}&link=${encodeURIComponent(item.link)}" 
               class="notion-study-button">
                Study
            </a>
        </div>
    `;

    return div;
}

// 错误处理
function handleError() {
    const categories = ['ai', 'entertainment', 'finance', 'politics'];
    categories.forEach(category => {
        const container = document.getElementById(`${category}-news`);
        if (container) {
            container.innerHTML = `
                <div class="notion-error">
                    <p>Failed to load news data</p>
                    <button onclick="location.reload()">Retry</button>
                </div>
            `;
        }
    });
}
