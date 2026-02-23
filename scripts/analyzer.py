import os
import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

def generate_trend_ideas(github_data, reddit_data, hn_data):
    """
    収集したデータを基にGemini 2.0 Flashを使って個人開発のアイデアやトレンドを抽出する
    """
    api_key = GEMINI_API_KEY

    if not api_key:
        print("エラー: GEMINI_API_KEY環境変数が設定されていません (.env を確認してください)。")
        return "エラー: GEMINI_API_KEYが見つかりません。"

    # 初期化
    client = genai.Client(api_key=api_key)
    
    # プロンプトの構築
    prompt = f"""
あなたは世界中のテック情報を分析する「超優秀なトレンドリサーチャー 兼 個人開発プランナー」です。
以下に提供される本日の「GitHub Trending」「Hacker News」と「Redditのテック界隈の投稿」の膨大なデータを分析し、以下の**【4つの分析軸】**に沿って情報を整理し、次に作るべきツールのアイデアを提案してください。

# 🎯 4つの分析軸（必須要件）
1. **タイムマシン（グローバルギャップ）:** 海外で話題になっている（なりかけている）が、日本でまだ話題になっていないツールや技術
2. **リアルなペイン（不満）:** エンジニア・非エンジニア問わず「これが不便」「こういうのが欲しい」と明確に困っていること
3. **便利な最新機能:** 今話題になっている、新しくて便利な機能やUI/UXのアプローチ
4. **AI最前線:** AI（LLM, Agent, 自動化など）に関するすべてのホットな話題や活用方法

# 📥 情報源データ
## GitHub Trending (本日急上昇中のリポジトリ)
{json.dumps(github_data, indent=2, ensure_ascii=False)}

## Hacker News (世界トップハッカーの議論・アイデア)
{json.dumps(hn_data, indent=2, ensure_ascii=False)}

## Reddit Top Posts (海外の需要・不満・サイドプロジェクト)
{json.dumps(reddit_data, indent=2, ensure_ascii=False)}

---
出力は綺麗なMarkdownフォーマット（日本語）で、以下の形式に従ってください。

## 🌐 今日のグローバルトレンド概況
（全体の傾向を1〜2段落でまとめる）

## 🎯 4つの分析軸に基づくハイライト
### 1. タイムマシン（海外で話題だが日本未上陸）
- [抽出した内容やツール名]
- [日本に持ち込んだ際にウケる理由]

### 2. リアルな不満と需要（解決すべきペイン）
- [具体的に誰が何に困っているか]
- [それを解決できそうなアプローチ]

### 3. 注目の便利機能・UI
- [目を引いた機能や実装アイデア]

### 4. AI最前線キャッチアップ
- [AI関連で話題になっていた概念やツール群]

## 🚀 次の個人開発アイデア (特におすすめの種を2〜3個)
### アイデア名: [簡潔でキャッチーな名前]
- **着想元:** [どの情報・軸から着想を得たか]
- **解決する課題:** [どのようなペインを解消するか]
- **作るべき理由:** [なぜ今、あなたが作るべきなのか]
"""

    print("Analyzing trends with Gemini 2.0 Flash...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error during Gemini generation: {e}")
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    # ダミーデータでのローカルテスト
    dummy_github = [{"repo": "test/ai-tool", "description": "Awesome AI tool"}]
    dummy_reddit = [{"title": "I hate organizing my tabs", "content": "Too many tabs..."}]
    result = generate_trend_ideas(dummy_github, dummy_reddit)
    print(result)
