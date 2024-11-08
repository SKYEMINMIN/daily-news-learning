import json
import os
import sys
import logging
import time
import random
import requests

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('study_processor.log'),
        logging.StreamHandler()
    ]
)

class SimpleTranslator:
    def __init__(self):
        self.base_url = "http://translate.googleapis.com/translate_a/single"
        
    def translate(self, text, from_lang='en', to_lang='zh-CN'):
        if not text:
            return ""
            
        try:
            params = {
                'client': 'gtx',
                'sl': from_lang,
                'tl': to_lang,
                'dt': 't',
                'q': text
            }
            
            # 添加随机延迟
            time.sleep(random.uniform(1, 2))
            
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result and len(result) > 0 and len(result[C_0]()) > 0:
                        return result[C_0]()[C_0]()[C_0]()
                except:
                    pass
            return "翻译失败"
            
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return "翻译失败"

class StudyProcessor:
    def __init__(self):
        self.translator = SimpleTranslator()
        
    def translate_text(self, text):
        """翻译文本"""
        if not text:
            return ""
            
        try:
            # 处理过长的文本
            if len(text) > 1000:  # 限制长度
                parts = [text[i:i+1000] for i in range(0, len(text), 1000)]
                translated_parts = []
                for part in parts:
                    time.sleep(1)  # 每个部分之间添加延迟
                    translated_parts.append(self.translator.translate(part))
                return ' '.join(translated_parts)
            return self.translator.translate(text)
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            return "翻译失败"

    def get_words(self, text):
        """简单的分词"""
        try:
            # 移除常见的标点符号和特殊字符
            for char in '.,?!-:;"\'()[]{}@#$%^&*+=<>~/\\':
                text = text.replace(char, ' ')
            # 分词并过滤
            words = [word.strip().lower() for word in text.split() 
                    if len(word.strip()) > 3 
                    and word.strip().isalnum()]
            return list(set(words))  # 去重
        except Exception as e:
            logging.error(f"Word extraction error: {str(e)}")
            return []

    def generate_vocabulary(self, text):
        """生成词汇表"""
        try:
            words = self.get_words(text)
            vocab_list = []
            
            # 只取前3个词
            for word in words[:3]:
                chinese = self.translate_text(word)
                if chinese != "翻译失败":
                    vocab_list.append({
                        'word': word,
                        'translation': chinese,
                    })
            
            return vocab_list
        except Exception as e:
            logging.error(f"Vocabulary generation error: {str(e)}")
            return []

    def split_sentences(self, text):
        """简单的分句"""
        try:
            # 处理常见的句子结束标记
            for end_mark in ['。', '！', '？']:
                text = text.replace(end_mark, '.')
            # 分割句子
            sentences = []
            for s in text.split('.'):
                s = s.strip()
                if s:
                    sentences.append(s + '.')
            return sentences
        except Exception as e:
            logging.error(f"Sentence splitting error: {str(e)}")
            return []

    def generate_questions(self, text):
        """生成简单问题"""
        try:
            sentences = self.split_sentences(text)
            questions = []
            
            # 只处理第一个句子
            for sent in sentences[:1]:
                words = self.get_words(sent)
                if words:
                    word_to_blank = words[C_0]()
                    blank_sent = sent.lower().replace(word_to_blank, '_____', 1)
                    questions.append({
                        'type': 'fill-in',
                        'question': blank_sent,
                        'answer': word_to_blank
                    })
            
            return questions
        except Exception as e:
            logging.error(f"Question generation error: {str(e)}")
            return []

    def process_news(self, news_item):
        """处理单条新闻"""
        try:
            content = news_item.get('content', '')
            if not content:
                return None

            # 只处理第一个段落
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()][:1]
            processed_paragraphs = []
            
            for para in paragraphs:
                if len(para) > 10:
                    processed_para = {
                        'english': para,
                        'chinese': self.translate_text(para),
                        'vocabulary': self.generate_vocabulary(para),
                        'questions': self.generate_questions(para)
                    }
                    processed_paragraphs.append(processed_para)
            
            return {
                'id': news_item.get('id', ''),
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
                return
                
            os.makedirs('data/study', exist_ok=True)
            file_path = f'data/study/{news_id}.json'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Successfully saved study content for {news_id}")
            
        except Exception as e:
            logging.error(f"Error saving study content: {str(e)}")

def main():
    try:
        if not os.path.exists('data/news.json'):
            logging.error("news.json not found")
            return False

        with open('data/news.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)

        processor = StudyProcessor()
        success_count = 0
        total_count = len(news_data)
        
        # 只处理前2条新闻
        for news_item in news_data[:2]:
            try:
                study_content = processor.process_news(news_item)
                if study_content:
                    processor.save_study_content(news_item.get('id', ''), study_content)
                    success_count += 1
            except Exception as e:
                logging.error(f"Error processing news: {str(e)}")
                continue

        logging.info(f"Processed {success_count} out of {total_count} news items successfully")
        return success_count > 0

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
