class StudyPage {
    constructor() {
        this.newsId = new URLSearchParams(window.location.search).get('id');
        this.newsData = null;
        this.vocabularyList = new Set();
    }

    async init() {
        try {
            await this.loadNewsData();
            await this.processContent();
            this.render();
        } catch (error) {
            console.error('Error initializing study page:', error);
            this.showError('Failed to load study content');
        }
    }

    async loadNewsData() {
        const response = await fetch('data/news.json');
        const data = await response.json();
        this.newsData = this.findNewsById(data);
        if (!this.newsData) {
            throw new Error('News not found');
        }
    }

    findNewsById(data) {
        for (const category of Object.values(data)) {
            const news = category.find(item => item.id === this.newsId);
            if (news) return news;
        }
        return null;
    }

    async processContent() {
        if (!this.newsData.processed) {
            // 分段处理
            this.newsData.paragraphs = this.splitIntoParagraphs(this.newsData.content);
            
            // 翻译处理
            for (let para of this.newsData.paragraphs) {
                para.translation = await this.translateText(para.text);
                para.processedText = this.processVocabulary(para.text);
            }

            // 生成词汇表
            this.newsData.vocabulary = await this.processVocabularyList();

            // 生成问题
            this.newsData.questions = this.generateQuestions();

            this.newsData.processed = true;
        }
    }

    splitIntoParagraphs(content) {
        return content.split(/\n\n+/).filter(p => p.trim()).map(text => ({
            text: text,
            translation: '',
            processedText: ''
        }));
    }

    async translateText(text) {
        // 这里应该调用翻译API
        // 演示用直接返回
        return `[Translation of: ${text}]`;
    }

    processVocabulary(text) {
        // 处理词汇，标记重点词
        const words = this.getKeyWords(text);
        let processedText = text;
        words.forEach(word => {
            this.vocabularyList.add(word);
            processedText = processedText.replace(
                new RegExp(`\\b${word}\\b`, 'gi'),
                `<span class="highlight-word" data-word="${word}">$&</span>`
            );
        });
        return processedText;
    }

    getKeyWords(text) {
        // 这里应该有一个中学生词汇表来匹配
        // 演示用简单实现
        return text.match(/\b[a-zA-Z]{7,}\b/g) || [];
    }

    async processVocabularyList() {
        const vocabList = [];
        for (const word of this.vocabularyList) {
            vocabList.push({
                word: word,
                phonetic: await this.getPhonetic(word),
                pos: await this.getPartOfSpeech(word),
                meaning: await this.getWordMeaning(word),
                example: await this.getWordExample(word)
            });
        }
        return vocabList;
    }

    generateQuestions() {
        return [
            {
                question: "What is the main idea of this article?",
                answer: "Based on the content, the main idea is..."
            },
            {
                question: "What are the key points mentioned?",
                answer: "The key points include..."
            },
            {
                question: "How does this relate to current events?",
                answer: "This relates to current events by..."
            }
        ];
    }

    render() {
        this.renderTitle();
        this.renderParagraphs();
        this.renderVocabulary();
        this.renderQuestions();
    }

    renderTitle() {
        document.getElementById('original-title').textContent = this.newsData.title;
        document.getElementById('translated-title').textContent = 
            this.newsData.translatedTitle || 'Loading translation...';
    }

    renderParagraphs() {
        const container = document.getElementById('paragraph-container');
        container.innerHTML = '';
        
        this.newsData.paragraphs.forEach((para, index) => {
            const div = document.createElement('div');
            div.className = 'notion-paragraph';
            div.innerHTML = `
                <div class="original-text">${para.processedText}</div>
                <div class="paragraph-translation">${para.translation}</div>
            `;
            container.appendChild(div);
        });
    }

    renderVocabulary() {
        const container = document.getElementById('vocabulary-container');
        container.innerHTML = '';
        
        this.newsData.vocabulary.forEach(word => {
            const div = document.createElement('div');
            div.className = 'vocab-card';
            div.innerHTML = `
                <div class="word-header">
                    <span class="word">${word.word}</span>
                    <span class="phonetic">${word.phonetic}</span>
                </div>
                <div class="word-pos">${word.pos}</div>
                <div class="word-meaning">${word.meaning}</div>
                <div class="word-example">${word.example}</div>
            `;
            container.appendChild(div);
        });
    }

    renderQuestions() {
        const container = document.getElementById('questions-container');
        container.innerHTML = '';
        
        this.newsData.questions.forEach((q, index) => {
            const div = document.createElement('div');
            div.className = 'question-card';
            div.innerHTML = `
                <div class="question">Q${index + 1}: ${q.question}</div>
                <div class="answer">A: ${q.answer}</div>
            `;
            container.appendChild(div);
        });
    }

    showError(message) {
        document.querySelector('.notion-container').innerHTML = `
            <div class="notion-error">
                <p>${message}</p>
                <button onclick="location.reload()">Retry</button>
            </div>
        `;
    }

    // 辅助方法 - 这些方法需要对接实际的API
    async getPhonetic(word) { return "[phonetic]"; }
    async getPartOfSpeech(word) { return "n./v./adj."; }
    async getWordMeaning(word) { return "词义"; }
    async getWordExample(word) { return "Example sentence."; }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    const studyPage = new StudyPage();
    studyPage.init();
});
