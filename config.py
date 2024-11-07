name: Update News

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        persist-credentials: true
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip'
        check-latest: true
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install --upgrade certifi
        pip install requests json2html pandas gnewsclient
    
    - name: Run update script
      env:
        NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
        PYTHONWARNINGS: "ignore:Unverified HTTPS request"
      run: |
        echo "Python version:"
        python --version
        # 更新证书
        python -m certifi
        python config.py
    
    - name: Commit and push if changed
      run: |
        git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
        git config --global user.name "github-actions[bot]"
        git add -A
        timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
        git commit -m "Update news data: ${timestamp}" || exit 0
        git push origin main

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
