import os
import datetime
import requests
from fetch_github import fetch_github_trending
from fetch_reddit import fetch_reddit_top_posts
from analyzer import generate_trend_ideas
from fetch_hackernews import fetch_hacker_news_top
from config import DISCORD_WEBHOOK_URL

def get_obsidian_trend_forge_path():
    """
    OAKのWorkspaceディレクトリのパスからTrendForge出力用フォルダを決定する
    """
    workspace_path = "C:\\Users\\swamp\\.gemini\\Antigravity-workspace"
    trend_dir = os.path.join(workspace_path, "Knowledge", "TrendForge")
    
    if not os.path.exists(trend_dir):
        os.makedirs(trend_dir, exist_ok=True)
        print(f"Created output directory: {trend_dir}")
        
    return trend_dir

def post_to_discord(content):
    """
    生成されたMarkdownレポートをDiscordへ送信する
    """
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL is not set. Skipping Discord notification.")
        return

    print("Sending report to Discord...")
    
    # Discordのメッセージ長制限（2000文字）に対応するため分割して送信
    # またはファイルとして添付する
    payload = {
        "content": "🚀 **今日のAIトレンド・リサーチレポートが届きました！**",
        "embeds": [
            {
                "title": f"💡 Trend Forge Report: {datetime.datetime.now().strftime('%Y-%m-%d')}",
                "description": content[:4000] + ("...\n(Truncated)" if len(content) > 4000 else ""),
                "color": 3447003
            }
        ]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("✅ Successfully sent to Discord.")
    except Exception as e:
        print(f"❌ Failed to send to Discord: {e}")

def main():
    print("="*40)
    print("🚀 Starting AI Trend Forge Process")
    print("="*40)
    
    # 1. データスクレイピング & API収集
    github_lang = "python" # 例: python界隈のトレンド
    # 新たに「AppIdeas(アプリ案)」や「SomebodyMakeThis(誰か作って)」を追加してペイン重視の構成に
    reddit_subs = ["SideProject", "AppIdeas", "SomebodyMakeThis", "macapps", "chrome_extensions"]
    
    print("\n[Step 1] Fetching raw data...")
    github_data = fetch_github_trending(language=github_lang, timeframe="daily")
    
    print("\nfetching Hacker News top stories...")
    hn_data = fetch_hacker_news_top(limit=10)
    
    reddit_data = []
    for sub in reddit_subs:
        data = fetch_reddit_top_posts(sub, limit=5)
        reddit_data.extend(data)
        
    print(f"✓ Collected {len(github_data)} GitHub repos, {len(hn_data)} Hacker News stories, and {len(reddit_data)} Reddit posts.")
    
    # 2. AIによる要約とアイデア生成
    print("\n[Step 2] Analyzing and generating ideas with Gemini 2.0 Flash...")
    markdown_report = generate_trend_ideas(github_data, reddit_data, hn_data)
    
    if markdown_report.startswith("エラー"):
        print("❌ Analysis failed.")
        return
        
    print("✓ Analysis complete.")
    
    # 3. Obsidianへの保存
    print("\n[Step 3] Saving to Obsidian (Knowledge/TrendForge/)...")
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    output_dir = get_obsidian_trend_forge_path()
    output_file = os.path.join(output_dir, f"TrendForge_{today_str}.md")
    
    # ヘッダーを付けて保存
    final_content = f"""---
tags:
  - type/knowledge
  - type/trend
created: {today_str}
---
# 💡 Trend Forge Report: {today_str}

このレポートはGitHub Trending (`{github_lang}`), Hacker News, そして Reddit (`{', '.join(reddit_subs)}`) の最新情報を**Gemini 2.0 Flash**が分析し、個人開発のインスピレーション源として自動生成したものです。

{markdown_report}
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Successfully saved report to: {output_file}")
    
    # 4. Discordへの通知
    print("\n[Step 4] Checking Discord Webhook...")
    post_to_discord(markdown_report)

    print("\n🚀 All done!")

if __name__ == "__main__":
    main()
