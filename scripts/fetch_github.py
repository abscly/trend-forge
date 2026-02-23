import requests
from bs4 import BeautifulSoup
import json
import datetime

def fetch_github_trending(language="all", timeframe="daily"):
    """
    GitHub Trendingから最新のリポジトリを取得する（スクレイピング）
    公式APIがないためBeautifulSoupを使用
    """
    url = f"https://github.com/trending/{language}?since={timeframe}"
    print(f"Fetching GitHub Trending ({language}, {timeframe})...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        repos = []
        for article in soup.find_all('article', class_='Box-row')[:10]: # 上位10件
            title_h2 = article.find('h2', class_='h3 lh-condensed')
            repo_link = title_h2.find('a')['href']
            repo_name = repo_link.lstrip('/')
            
            description_p = article.find('p', class_='col-9 color-fg-muted my-1 pr-4')
            description = description_p.text.strip() if description_p else "No description"
            
            # 言語とスター数を取得
            lang_span = article.find('span', itemprop='programmingLanguage')
            language = lang_span.text.strip() if lang_span else "Unknown"
            
            star_a = article.find('a', href=f"{repo_link}/stargazers")
            stars = star_a.text.strip().replace(',', '') if star_a else "0"
            
            repos.append({
                "repo": repo_name,
                "url": f"https://github.com/{repo_name}",
                "description": description,
                "language": language,
                "stars_today": stars,
                "source": "GitHub Trending"
            })
            
        return repos

    except Exception as e:
        print(f"Error fetching GitHub Trending: {e}")
        return []

if __name__ == "__main__":
    # テスト実行
    data = fetch_github_trending("python")
    print(json.dumps(data, indent=2, ensure_ascii=False))
