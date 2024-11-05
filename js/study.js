class NewsLearningProcessor {
    constructor(newsText) {
        this.newsText = newsText;
        this.paragraphs = this.splitIntoParagraphs(newsText);
        this.vocabulary = new Set();
    }

    // 将新闻分段
    splitIntoParagraphs(text) {
        return text.split(/\n\n+/).filter(p => p.trim());
    }

    // 处理单个段落
    async processParagraph(paragraph) {
        try {
            // 调用翻译API获取中文翻译
            const translation = await this.translateText(paragraph);
            
            // 识别重点词汇
            const highlightedText = this.highlightKeywords(paragraph);
            
            return {
                original: highlightedText,
                translation: translation,
            };
        } catch (error) {
            console.error('Error processing paragraph:', error);
            return null;
        }
    }

    // 高亮关键词
    highlightKeywords(text) {
        // 这里可以加入一个中学生词汇表来匹配重点词
        const keywords = this.identifyKeywords(text);
        keywords.forEach(word => this.vocabulary.add(word));
        
        return text.replace(/\b\w+\b/g, word => {
            if (keywords.includes(word.toLowerCase())) {
                return `<span class="highlight-word" data-word="${word}">${word}</span>`;
            }
            return word;
        });
    }

    // 生成理解问题
    generateQuestions() {
        return [
            {
                question: "What is the main topic of this news?",
                answer: "..." // 根据文章内容生成
            },
            {
                question: "What are the key points mentioned in the article?",
                answer: "..."
            },
            {
                question: "How does this news affect our daily life?",
                answer: "..."
            }
        ];
    }

    // 处理词汇
    async processVocabulary() {
        const vocabList = [];
        for (const word of this.vocabulary) {
            // 调用词典API获取词汇详细信息
            const wordInfo = await this.getWordInfo(word);
            vocabList.push({
                word: word,
                phonetic: wordInfo.phonetic,
                pos: wordInfo.partOfSpeech,
                meaning: wordInfo.meaning,
                example: wordInfo.example
            });
        }
        return vocabList;
    }
}

// 页面初始化
async function initStudyPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const newsLink = urlParams.get('link');
    
    try {
        // 获取新闻内容
        const newsContent = await fetchNewsContent(newsLink);
        
        // 创建学习处理器
        const learningProcessor = new NewsLearningProcessor(newsContent);
        
        // 处理每个段落
        const paragraphsContainer = document.getElementById('paragraph-container');
        for (const paragraph of learningProcessor.paragraphs) {
            const processed = await learningProcessor.processParagraph(paragraph);
            if (processed) {
                const paragraphElement = createParagraphElement(processed);
                paragraphsContainer.appendChild(paragraphElement);
            }
        }
        
        // 处理词汇
        const vocabulary = await learningProcessor.processVocabulary();
        displayVocabulary(vocabulary);
        
        // 生成理解问题
        const questions = learningProcessor.generateQuestions();
        displayQuestions(questions);
        
    } catch (error) {
        console.error('Error initializing study page:', error);
    }
}

// 创建段落元素
function createParagraphElement(processedParagraph) {
    const element = document.createElement('div');
    element.className = 'notion-paragraph';
    element.innerHTML = `
        <div class="original">${processedParagraph.original}</div>
        <div class="translation">${processedParagraph.translation}</div>
    `;
    return element;
}

// 显示词汇表
function displayVocabulary(vocabulary) {
    const container = document.getElementById('vocabulary-container');
    vocabulary.forEach(word => {
        const wordElement = document.createElement('div');
        wordElement.className = 'notion-word-card';
        wordElement.innerHTML = `
            <div class="word">${word.word}</div>
            <div class="phonetic">${word.phonetic}</div>
            <div class="pos">${word.pos}</div>
            <div class="meaning">${word.meaning}</div>
            <div class="example">${word.example}</div>
        `;
        container.appendChild(wordElement);
    });
}

// 显示理解问题
function displayQuestions(questions) {
    const container = document.getElementById('questions-container');
    questions.forEach(q => {
        const questionElement = document.createElement('div');
        questionElement.className = 'notion-question';
        questionElement.innerHTML = `
            <div class="question">${q.question}</div>
            <div class="answer">${q.answer}</div>
        `;
        container.appendChild(questionElement);
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initStudyPage);
