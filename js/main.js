async function loadAllNews() {
    try {
        const response = await fetch('data/news.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.news;
    } catch (error) {
        console.error('Error loading news:', error);
        throw error;
    }
}

function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            timeZoneName: 'short'
        }).format(date);
    } catch (error) {
        console.error('Error formatting date:', error);
        return 'Date unavailable';
    }
}

async function updateNews() {
    try {
        const newsData = await loadAllNews();
        
        // Update datetime
        const datetimeElement = document.getElementById('datetime');
        datetimeElement.textContent = new Date().toLocaleString();
        
        // Update each news section
        const categories = ['ai', 'entertainment', 'finance', 'politics'];
        categories.forEach(category => {
            const newsElement = document.getElementById(`${category}-news`);
            if (newsData[category]) {
                const news = newsData[category];
                newsElement.innerHTML = `
                    <h3><a href="${news.url}" target="_blank">${news.title}</a></h3>
                    <p>Source: ${news.source}</p>
                    <p>Published: ${formatDate(news.time)}</p>
                `;
            } else {
                newsElement.innerHTML = '<p>No news available</p>';
            }
        });
    } catch (error) {
        // 显示错误信息在页面上
        document.querySelectorAll('.notion-news-container').forEach(container => {
            container.innerHTML = '<p class="error">Failed to load news. Please try again later.</p>';
        });
    }
}

// 初始加载
document.addEventListener('DOMContentLoaded', updateNews);

// 每5分钟刷新一次
setInterval(updateNews, 5 * 60 * 1000);
