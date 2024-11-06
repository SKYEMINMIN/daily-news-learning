import json
import os
import sys
import logging
import ssl
import nltk
from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

# 设置SSL上下文
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('study_processor.log'),
        logging.StreamHandler()
    ]
)

def download_nltk_data():
    """下载NLTK需要的数据"""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('words', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        return True
    except Exception as e:
        logging.error(f"Error downloading NLTK data: {str(e)}")
        return False

class StudyProcessor:
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='zh-CN')
        
    def translate_text(self, text):
        """翻译文本"""
        try:
            return self.translator.translate(text)
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return "翻译失败"

    def generate_vocabulary(self, text):
        """生成词汇表"""
        try:
            words = word_tokenize(text.lower())
            tagged = pos_tag(words)
            vocab_list = []
            
            for word, tag in tagged:
                if tag.startswith(('NN', 'VB', 'JJ', 'RB')) and len(word) > 3:
                    chinese = self.translate_text(word)
                    vocab_list.append({
                        'word': word,
                        'translation': chinese,
                        'pos': tag
                    })
            
            return vocab_list[:10]  # 返回前
