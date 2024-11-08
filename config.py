import os  

# Project root directory  
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  

# News data configuration  
NEWS_DATA_CONFIG = {  
    "data_dir": os.path.join(PROJECT_ROOT, "data"),  
    "news_file": "news-2024-11-06.json"  
}  

# News scraper configuration  
NEWS_SCRAPER_CONFIG = {  
    "url": "https://example.com/news",  
    "selectors": {  
        "title": ".news-title",  
        "content": ".news-content",  
        "published_at": ".news-date"  
    }  
}  

# News API configuration  
NEWS_API_CONFIG = {  
    "api_key": "dc6b340bb21432e40ed552ac70befd79",  
    "language": "zh",  
    "country": "cn",  
    "max_results": 10  
}  

# Output file configuration  
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "news.html")  

# Database configuration  
DATABASE_CONFIG = {  
    "host": "localhost",  
    "port": 5432,  
    "user": "your_username",  
    "password": "your_password",  
    "database": "news_db"  
}
