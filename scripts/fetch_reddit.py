import requests
import json

def fetch_reddit_top_posts(subreddit, limit=10, timeframe="day"):
    """
    指定されたSubredditからトップ投稿を取得する (JSON API)
    """
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t={timeframe}"
    print(f"Fetching Reddit top posts from r/{subreddit}...")
    
    # Reddit API requires a custom User-Agent to avoid 429 Too Many Requests
    headers = {
        "User-Agent": "TrendForge/1.0 (by abscly)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data.get("data", {}).get("children", []):
            post_data = child.get("data", {})
            
            # 除外: ピン留めや広告
            if post_data.get("stickied") or post_data.get("is_video"):
                continue
                
            title = post_data.get("title", "")
            selftext = post_data.get("selftext", "")
            url = post_data.get("url", "")
            score = post_data.get("score", 0)
            num_comments = post_data.get("num_comments", 0)
            
            # 短すぎる本文は除外 (画像メインの投稿など)
            # またはタイトルだけで意味が通じるものはOKとする
            content = f"{title}\n{selftext}"
            if len(content) > 2000:
                content = content[:2000] + "...(truncated)"
            
            posts.append({
                "subreddit": subreddit,
                "title": title,
                "content": content,
                "url": url,
                "score": score,
                "comments": num_comments,
                "source": "Reddit"
            })
            
        return posts

    except Exception as e:
        print(f"Error fetching Reddit (r/{subreddit}): {e}")
        return []

if __name__ == "__main__":
    # テスト: サイドプロジェクトやChrome拡張界隈の需要を探る
    data = fetch_reddit_top_posts("SideProject", limit=5)
    print(json.dumps(data, indent=2, ensure_ascii=False))
