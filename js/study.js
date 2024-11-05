// 获取URL参数中的新闻ID
function getNewsId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// 初始化页面
async function initStudyPage() {
    const newsId = getNewsId();
    if (!newsId) {
        alert('News ID not found');
        window.location.href = 'index.html';
        return;
    }

    try {
        // 这里后续我们会添加加载新闻数据的逻辑
        console.log('Loading news with ID:', newsId);
    } catch (error) {
        console.error('Error loading news:', error);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initStudyPage);
