// 修改 getNews 函数添加调试信息
async function getNews(category) {
    try {
        console.log(`Fetching news for ${category}...`);
        const response = await fetch(`data/${category.toLowerCase()}.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(`News data for ${category}:`, data);
        return data;
    } catch (error) {
        console.error(`Error loading ${category} news:`, error);
        return null;
    }
}

// 修改加载函数添加错误处理
async function loadCategoryNews() {
    const categories = ['AI', 'Entertainment', 'Finance', 'Politics'];
    
    for (const category of categories) {
        const newsContainer = document.getElementById(`${category.toLowerCase()}-news`);
        if (!newsContainer) {
            console.error(`Container for ${category} not found!`);
            continue;
        }
        
        newsContainer.innerHTML = '<div class="notion-loading">Loading news...</div>';
        
        try {
            const news = await getNews(category);
            if (news) {
                newsContainer.innerHTML = createNewsCard(news);
            } else {
                newsContainer.innerHTML = `
                    <div class="notion-error">
                        No news available for ${category}
                    </div>`;
            }
        } catch (error) {
            console.error(`Error processing ${category} news:`, error);
            newsContainer.innerHTML = `
                <div class="notion-error">
                    Error loading ${category} news: ${error.message}
                </div>`;
        }
    }
}

// 确保 DOM 加载后立即执行
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    updateDateTime();
    loadCategoryNews();
    setInterval(updateDateTime, 60000);
});
