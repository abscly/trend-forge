import requests
from bs4 import BeautifulSoup
import json

def fetch_hacker_news_top(limit=10):
    """
    Hacker News (Y Combinator) のトップストーリーを取得する（公式無料API）
    """
    print(f"Fetching Hacker News top posts...")
    
    try:
        # まずトップストーリーのID一覧を取得
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        posts = []
        for story_id in story_ids:
            # 各ストーリーの詳細を取得
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_resp = requests.get(story_url)
            story_data = story_resp.json()
            
            if not story_data:
                continue
                
            title = story_data.get("title", "")
            url = story_data.get("url", "")
            score = story_data.get("score", 0)
            
            # Show HN や Ask HN などのプレフィックス付きは特に需要が高い
            content = title
            if "text" in story_data:
                # Ask HN などは本文がある
                text = story_data["text"]
                # HTMLタグを簡易的に除去
                text = BeautifulSoup(text, "html.parser").get_text()
                content = f"{title}\n{text}"
                
            if len(content) > 1000:
                content = content[:1000] + "...(truncated)"
                
            posts.append({
                "title": title,
                "content": content,
                "url": url,
                "score": score,
                "source": "Hacker News"
            })
            
        return posts

    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
        return []

if __name__ == "__main__":
    # テスト
    data = fetch_hacker_news_top(limit=3)
    print(json.dumps(data, indent=2, ensure_ascii=False))
