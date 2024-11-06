import json
import os
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import words, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

class StudyProcessor:
    def __init__(self):
        # 下载必要的NLTK数据
        nltk.download('punkt')
        nltk.download('words')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        
        # 初始化翻译器
        self.translator = GoogleTranslator(source='en', target='zh-CN')
        
        # 加载英语常用词集合
        self.english_words = set(words.words())
        
    def translate_text(self, text):
        """使用Google Translate API进行翻译"""
        try:
            return self.translator.translate(text)
        except:
            return "翻译失败"
    
    def get_word_info(self, word):
        """获取单词信息"""
        syns = wordnet.synsets(word)
        if not syns:
            return None
            
        pos_map = {
            'n': '名词',
            'v': '动词',
            'a': '形容词',
            'r': '副词',
            's': '形容词卫星'
        }
        
        word_info = {
            'word': word,
            'pos': pos_map.get(syns[C_0]().pos(), '未知'),
            'translation': self.translate_text(word)
        }
        return word_info
    
    def process_paragraph(self, paragraph):
        """处理单个段落"""
        # 分词
        words = word_tokenize(paragraph)
        
        # 获取重要单词
        important_words = []
        for word in words:
            # 只处理字母组成的单词
            if not word.isalpha():
                continue
            # 排除常见简单词
            if word.lower() not in self.english_words or len(word) <= 3:
                continue
            
            word_info = self.get_word_info(word.lower())
            if word_info:
                important_words.append(word_info)
        
        return {
            'english': paragraph,
            'chinese': self.translate_text(paragraph),
            'vocabulary': important_words
        }
    
    def generate_questions(self, content):
        """生成简单的理解问题"""
        sentences = sent_tokenize(content)
        questions = []
        
        # 生成3个基本问题
        if sentences:
            questions.append({
                'question': "What is the main topic of this article?",
                'answer': "This article mainly discusses " + self.translate_text(sentences[C_0]())
            })
        
        if len(sentences) > 1:
            questions.append({
                'question': "What is one key point mentioned in the article?",
                'answer': "One key point is " + self.translate_text(sentences[C_1]())
            })
        
        questions.append({
            'question': "Why is this news significant?",
            'answer': "This news is significant because it affects/shows/demonstrates..."
        })
        
        return questions
    
    def process_news(self, news_item):
        """处理新闻内容"""
        # 分段
        paragraphs = news_item['content'].split('\n\n')
        
        # 处理每个段落
        processed_paragraphs = []
        all_vocabulary = []
        
        for para in paragraphs:
            if not para.strip():
                continue
                
            processed = self.process_paragraph(para)
            processed_paragraphs.append(processed)
            all_vocabulary.extend(processed['vocabulary'])
        
        # 生成理解问题
        questions = self.generate_questions(news_item['content'])
        
        # 创建学习内容
        study_content = {
            'title': news_item['title'],
            'paragraphs': processed_paragraphs,
            'vocabulary': list({v['word']: v for v in all_vocabulary}.values()),  # 去重
            'questions': questions
        }
        
        return study_content
    
    def save_study_content(self, news_id, study_content):
        """保存学习内容"""
        os.makedirs('data/study', exist_ok=True)
        with open(f'data/study/{news_id}.json', 'w', encoding='utf-8') as f:
            json.dump(study_content, f, ensure_ascii=False, indent=2)

def main():
    # 读取新闻数据
    with open('data/news.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    processor = StudyProcessor()
    
    # 处理每条新闻
    for news in news_data:
        study_content = processor.process_news(news)
        processor.save_study_content(news['id'], study_content)

if __name__ == "__main__":
    main()
