name: daily-update.yml

on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行
  workflow_dispatch:      # 允许手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write     # 明确指定写入权限

    steps:
    - uses: actions/checkout@v4    # checkout 目前最新稳定版是 v4
    
    - name: Set up Python
      uses: actions/setup-python@v5   # 更新到 v5
      with:
        python-version: '3.12'    # 使用最新的 Python 3.12
        cache: 'pip'              # 启用 pip 缓存
        check-latest: true        # 检查最新的补丁版本
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
    
    - name: Run update script
      env:
        NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
      run: |
        echo "Python version:"
        python --version
        python config.py
    
    - name: Commit and push if changed
      run: |
        git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
        git config --global user.name "github-actions[bot]"
        git add -A
        timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
        git commit -m "Update news data: ${timestamp}" || exit 0
        git push

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
