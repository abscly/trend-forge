import requests
import base64
from config import GITHUB_TOKEN, VAULT_REPO

def upload_to_vault(filename, content):
    """
    GitHub REST APIを使用して、生成されたTrendForgeレポートを
    直接Vault（リポジトリ）の特定のディレクトリにコミット・プッシュする
    """
    if not GITHUB_TOKEN:
        print("⚠️ GITHUB_TOKEN is not set. Skipping GitHub Vault upload (Saving locally only).")
        return False

    url = f"https://api.github.com/repos/{VAULT_REPO}/contents/Knowledge/TrendForge/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # APIはコンテンツをBase64エンコードで受け付ける
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": f"🤖 Auto-saving TrendForge report: {filename} from GCE",
        "content": encoded_content
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ Successfully saved {filename} to GitHub Vault ({VAULT_REPO}).")
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            print(f"⚠️ 422 Error: File {filename} already exists in Vault, or validation failed.")
        else:
            print(f"❌ Failed to upload to GitHub Vault HTTP {e.response.status_code}: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Failed to upload to GitHub Vault: {e}")
        return False
