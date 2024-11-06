import json
import os
import sys
import logging
import nltk
from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('study_processor.log'),
        logging.StreamHandler()
    ]
)

# 下载必要的NLTK数据
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

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
            
            return vocab_list[:10]  # 返回前10个词
        except Exception as e:
            logging.error(f"Vocabulary generation error: {str(e)}")
            return []

    def generate_questions(self, text):
        """生成简单问题"""
        try:
            sentences = sent_tokenize(text)
            questions = []
            
            for sent in sentences[:3]:  # 只处理前3个句子
                # 生成填空题
                words = word_tokenize(sent)
                tagged = pos_tag(words)
                
                for i, (word, tag) in enumerate(tagged):
                    if tag.startswith(('NN', 'VB')) and len(word) > 3:
                        blank_sent = ' '.join(words[:i] + ['_____'] + words[i+1:])
                        questions.append({
                            'type': 'fill-in',
                            'question': blank_sent,
                            'answer': word
                        })
                        break  # 每个句子只生成一个问题
            
            return questions
        except Exception as e:
            logging.error(f"Question generation error: {str(e)}")
            return []

    def process_news(self, news_item):
        """处理单条新闻"""
        try:
            # 验证输入数据
            if not isinstance(news_item, dict):
                logging.error(f"Invalid news item type: {type(news_item)}")
                return None

            # 获取并验证内容
            content = news_item.get('content')
            if not content:
                logging.error(f"No content found for news item: {news_item.get('id', 'unknown')}")
                return None

            # 确保内容是字符串
            if not isinstance(content, str):
                logging.error(f"Invalid content type: {type(content)}")
                return None

            # 按段落分割内容
            paragraphs = content.split('\n\n')
            
            # 处理每个段落
            processed_paragraphs = []
            for para in paragraphs:
                if para.strip():  # 忽略空段落
                    processed_para = {
                        'english': para.strip(),
                        'chinese': self.translate_text(para.strip()),
                        'vocabulary': self.generate_vocabulary(para),
                        'questions': self.generate_questions(para)
                    }
                    processed_paragraphs.append(processed_para)
            
            return {
                'id': news_item.get('id', 'unknown'),
                'title': news_item.get('title', ''),
                'paragraphs': processed_paragraphs
            }
            
        except Exception as e:
            logging.error(f"Error processing news item: {str(e)}")
            return None

    def save_study_content(self, news_id, content):
        """保存学习内容"""
        try:
            if content is None:
                logging.error(f"No content to save for news ID: {news_id}")
                return
                
            # 确保目录存在
            os.makedirs('data/study', exist_ok=True)
            
            # 保存文件
            file_path = f'data/study/{news_id}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Successfully saved study content for {news_id}")
            
        except Exception as e:
            logging.error(f"Error saving study content: {str(e)}")

def main():
    try:
        # 确保news.json存在
        if not os.path.exists('data/news.json'):
            logging.error("news.json not found")
            return False

        # 读取新闻数据
        with open('data/news.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)

        if not isinstance(news_data, list):
            logging.error("News data is not in the expected format")
            return False

        processor = StudyProcessor()

        for news_item in news_data:
            if not isinstance(news_item, dict):
                logging.error(f"Invalid news item format: {news_item}")
                continue

            try:
                logging.info(f"Processing news item: {news_item.get('id', 'unknown')}")
                study_content = processor.process_news(news_item)
                if study_content:
                    processor.save_study_content(news_item.get('id', 'unknown'), study_content)
                    logging.info(f"Successfully processed news {news_item.get('id', 'unknown')}")
            except Exception as e:
                logging.error(f"Error processing news {news_item.get('id', 'unknown')}: {str(e)}")
                continue

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
