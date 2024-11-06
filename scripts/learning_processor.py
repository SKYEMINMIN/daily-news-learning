import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from datetime import datetime
import requests

class LearningMaterialGenerator:
    def __init__(self):
        # 确保下载必要的NLTK数据
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

        # 加载基础词汇表（中学生应该掌握的词汇）
        self.basic_words = self._load_basic_words()
        
    def _load_basic_words(self):
        # 这里可以从文件加载，现在先返回示例
        return set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that'])

    def process_text(self, text):
        # 分段
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        processed_paragraphs = []
        
        for para in paragraphs:
            processed_para = {
                "english": para,
                "chinese": self._translate_text(para),
                "keywords": self._extract_keywords(para)
            }
            processed_paragraphs.append(processed_para)
            
        return processed_paragraphs

    def _translate_text(self, text):
        try:
            # 使用Google翻译API
            url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                "q": text,
                "target": "zh",
                "source": "en"
            }
            response = requests.post(url, params=params)
            return response.json()['data']['translations'][C_0]()['translatedText']
        except:
            return "Translation failed"

    def _extract_keywords(self, text):
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        keywords = []
        for word, pos in pos_tags:
            if (word.lower() not in self.basic_words and 
                len(word) > 3 and 
                word.isalnum()):
                
                keyword = {
                    "word": word,
                    "phonetic": self._get_phonetic(word),
                    "pos": self._convert_pos_tag(pos),
                    "meaning": self._get_word_meaning(word),
                    "example": self._get_example(word)
                }
                keywords.append(keyword)
        
        return keywords

    def _get_phonetic(self, word):
        # 这里可以接入词典API
        return "/示例音标/"

    def _convert_pos_tag(self, pos):
        # 转换词性标注为更易读的格式
        pos_dict = {
            'NN': 'n.',
            'VB': 'v.',
            'JJ': 'adj.',
            'RB': 'adv.'
        }
        return pos_dict.get(pos[:2], pos)

    def _get_word_meaning(self, word):
        # 这里可以接入词典API
        return "示例释义"

    def _get_example(self, word):
        # 这里可以接入例句API
        return f"This is an example sentence with {word}."

    def generate_questions(self, text):
        # 生成理解问题
        return [
            {
                "question": "What is the main idea of this article?",
                "answer": "The main idea is..."
            },
            {
                "question": "What are the key points discussed?",
                "answer": "The key points are..."
            },
            {
                "question": "How might this impact society?",
                "answer": "This might impact society by..."
            }
        ]
