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
出力は綺麗なMarkdownフォーマット（日本語）で、以下の構造を厳格に守って出力してください。
忙しいエンジニアがスマホ（Discord）でパッと見て直感的に理解できるよう、**箇条書き、太字、絵文字を多用して視覚的にメリハリをつける**こと。

## 🌐 今日のグローバルトレンド概況
> （全体の傾向や熱狂している技術を、**力強い太字**を交えて1〜2段落でまとめる）

## 🎯 4つの分析軸に基づくハイライト
### 🕰️ 1. タイムマシン（海外で話題だが日本未上陸）
- **[注目ツール/技術名]**
  - **内容:** [簡潔な説明]
  - **日本での勝機:** [なぜ日本に持ち込んだ際にウケるのか]

### 🤕 2. リアルな不満と需要（解決すべきペイン）
- **[ペインの核心]**
  - **誰が困っているか:** [対象ユーザー]
  - **解決の糸口:** [どう作れば解決するか]

### 💡 3. 注目の便利機能・UI
- **[機能のコンセプト]**
  - **着眼点:** [どこが優れている・新しいか]

### 🤖 4. AI最前線キャッチアップ
- **[AI関連の注目トピック]**
  - **インパクト:** [開発にどう活かせるか]

---
## 👤 今話題の人物・キープレイヤー (Sources)
（今回のデータソースの中で、特に目立っている発言者、開発者、企業、または頻繁に引用されている情報源を1〜2つピックアップ）
- **[人物/企業/プロジェクト名]**
  - **何者か:** [一言で説明]
  - **なぜ注目されているか:** [彼らが発信・作成した内容と、界隈からの反響]

---
## 🚀 次の個人開発アイデア (特におすすめの種)
今回は、情報源から「エンジニア向け」と「非エンジニア（一般・生活）向け」の需要をそれぞれ必ず1つ以上抽出して提案してください。

### 💻 【エンジニア向け】 アイデア名: [キャッチーな名前]
- 💡 **着想元:** [どの情報源・軸から来たか]
- 🎯 **ターゲット:** [どんな開発者やテック層か]
- 痛 **解決する課題:** [どんなペインを消すか]
- 🛠️ **技術スタック:** [実装方法のヒント]
- 🔥 **なぜあなたが今作るべきか:** [モチベーションが上がる一言]

### 🏡 【一般・生活向け】 アイデア名: [キャッチーな名前]
- 💡 **着想元:** [どの情報源（LifeProTipsやproductivity等）から来たか]
- 🎯 **ターゲット:** [どんな一般の人・職種か]
- 痛 **解決する生活の課題:** [どんな日常の不満や面倒を消すか]
- 📱 **提供形態のヒント:** [Webアプリ、拡張機能、ショートカット等]
- 🔥 **一般層にウケる理由:** [なぜ彼らがこれにお金を払う（または熱狂する）のか]

---
## 📝 今日のまとめ・考察 (Next Action)
> （今日のリサーチ全体を通して言える傾向と、**「開発者は今日何から始めるべきか」**という熱いアドバイス・考察を最後に1段落でまとめる。ここでDiscordの3ページ目を見事に締めくくること）
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
