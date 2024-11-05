class StudyPage {
    constructor() {
        this.newsId = new URLSearchParams(window.location.search).get('id');
        this.newsData = null;
    }

    async init() {
        await this.loadNewsData();
        this.renderPage();
    }

    async loadNewsData() {
        const response = await fetch('data/news.json');
        const data = await response.json();
        // Find the news item by ID
        for (const category of Object.values(data)) {
            const news = category.find(item => item.id === this.newsId);
            if (news) {
                this.newsData = news;
                break;
            }
        }
    }

    renderPage() {
        if (!this.newsData) return;

        // Render titles
        document.getElementById('originalTitle').textContent = this.newsData.title;
        document.getElementById('translatedTitle').textContent = this.newsData.translation.title;

        // Render paragraphs
        this.renderParagraphs();

        // Render vocabulary
        this.renderVocabulary();

        // Render questions
        this.renderQuestions();
    }

    renderParagraphs() {
        const container = document.getElementById('contentSection');
        this.newsData.translation.paragraphs.forEach(para => {
            const div = document.createElement('div');
            div.className = 'notion-paragraph';
            div.innerHTML = `
                <div class="original">${this.highlightVocabulary(para.original)}</div>
                <div class="translation">${para.translated}</div>
            `;
            container.appendChild(div);
        });
    }

    highlightVocabulary(text) {
        const vocab = this.newsData.vocabulary.map(v => v.word);
        return text.replace(new RegExp(`\\b(${vocab.join('|')})\\b`, 'gi'), 
            '<span class="highlight-word">$1</span>');
    }

    renderVocabulary() {
        const container = document.getElementById('vocabularyList');
        this.newsData.vocabulary.forEach(word => {
            const div = document.createElement('div');
            div.className = 'vocab-card';
            div.innerHTML = `
                <div class="word">${word.word}</div>
                <div class="phonetic">${word.phonetic}</div>
                <div class="pos">${word.pos}</div>
                <div class="meaning">${word.meaning}</div>
                <div class="example">${word.example}</div>
            `;
            container.appendChild(div);
        });
    }

    renderQuestions() {
        const container = document.getElementById('questionsList');
        this.newsData.questions.forEach(q => {
            const div = document.createElement('div');
            div.className = 'question-item';
            div.innerHTML = `
                <div class="question">${q.question}</div>
                <div class="answer">${q.answer}</div>
            `;
            container.appendChild(div);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const studyPage = new StudyPage();
    studyPage.init();
});
