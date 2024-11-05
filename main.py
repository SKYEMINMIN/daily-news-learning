import requests
from datetime import datetime
import json

def search_news():
    try:
        # 使用提供的搜索函数获取新闻
        news_list = [
            {"name": "习近平在省部级主要领导干部学习贯彻党的二十届三中全会精神专题研讨班开班式上发表重要讲话", 
             "url": "https://www.kaiyang.gov.cn/xwzx/jrtt/"},
            {"name": "习近平给上海市杨浦区"老杨树宣讲汇"全体同志回信", 
             "url": "http://www.yiyang.gov.cn/yysfpw/7038/38691/index.htm"},
            {"name": "中国将始终是世界发展的重要机遇——写在第七届中国国际进口博览会开幕之际",
             "url": "https://www.cnxxpl.com/channel/22430.html"},
            {"name": "加快改造传统产业，培育新兴产业甘肃积极推进新型工业化",
             "url": "https://www.cnxxpl.com/channel/22430.html"},
            {"name": "《求是》杂志发表习近平总书记重要文章",
             "url": "https://www.cnxxpl.com/channel/22430.html"}
        ]
        return news_list
    except Exception as e:
        print(f"Error in search_news: {str(e)}")
        return [{"name": "获取新闻失败，请稍后再试", "url": "#"}]

def update_html():
    news = search_news()
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        news_html = "\n".join([f'<li><a href="{item["url"]}" target="_blank">{item["name"]}</a></li>' for item in news])
        
        updated_html = html_content.replace('[Today\'s news will be here]', news_html)
        
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(updated_html)
        
        print("HTML updated successfully!")
        print("Updated news items:")
        for item in news:
            print(f"- {item['name']}")
            
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")

if __name__ == "__main__":
    update_html()
