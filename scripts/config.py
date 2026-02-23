import os
from dotenv import load_dotenv

# ローカルでもGCEでも有効に働くように.envを読み込む
load_dotenv()

# Discord Webhook URL
# 例: https://discord.com/api/webhooks/xxxxx/yyyyy
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# GitHub API Token for Vault Commit
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Vault Reposiotry Name (e.g. "abscly/Antigravity-workspace")
VAULT_REPO = os.getenv("VAULT_REPO", "abscly/Antigravity-workspace")
