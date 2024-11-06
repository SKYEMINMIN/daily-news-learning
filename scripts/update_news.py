name: Update News

on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行
  workflow_dispatch:      # 允许手动触发

jobs:
  update-news:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 1
        
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests nltk deep-translator
        
    - name: Create Directories
      run: |
        mkdir -p data
        mkdir -p data/study
        
    - name: Update news
      run: |
        python scripts/update_news.py
        
    - name: Process study materials
      run: |
        python scripts/study_processor.py
        
    - name: Configure Git
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        
    - name: Commit and Push
      run: |
        git add -A
        git commit -m "Auto update news [skip ci]" || echo "No changes to commit"
        git push || {
          git fetch origin
          git reset --hard origin/main
          git add -A
          git commit -m "Auto update news [skip ci]" || echo "No changes to commit"
          git push
        }
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
