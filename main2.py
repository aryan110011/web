import requests
import time
import random
import re
import os

# ------------ CONFIG ------------
PASSWORD = "aryan123"
# --------------------------------

def check_password():
    pw = input("🔒 Enter Script Password: ")
    if pw != PASSWORD:
        print("❌ Incorrect password!")
        exit()

def print_logo():
    print("""
█████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║
███████║██████╔╝██║   ██║███████║██╔██╗ ██║
██╔══██║██╔═══╝ ██║   ██║██╔══██║██║╚██╗██║
██║  ██║██║     ╚██████╔╝██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
🔥 Facebook Auto Comment Tool by Aryan 🔥
""")

def get_token_from_cookie(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie
    }
    try:
        res = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = re.search(r'"EAAG\w+', res.text)
        if token:
            return token.group(0)
    except:
        return None

def get_user_name(token):
    try:
        res = requests.get(f"https://graph.facebook.com/me?access_token={token}").json()
        return res.get("name", "Unknown")
    except:
        return "Unknown"

def get_post_ids_from_wall(token, limit=10):
    try:
        url = f"https://graph.facebook.com/me/feed?limit={limit}&access_token={token}"
        res = requests.get(url).json()
        return [p['id'] for p in res.get("data", [])]
    except:
        return []

def get_page_list(token):
    url = f"https://graph.facebook.com/me/accounts?access_token={token}"
    try:
        res = requests.get(url).json()
        pages = {}
        for page in res.get("data", []):
            pages[page["name"]] = {
                "id": page["id"],
                "token": page["access_token"]
            }
        return pages
    except:
        return {}

def comment_post(token, post_id, message):
    url = f"https://graph.facebook.com/{post_id}/comments"
    data = {
        "message": message,
        "access_token": token
    }
    try:
        res = requests.post(url, data=data).json()
        return res
    except:
        return {"error": "network error"}

def load_lines(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return []
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_tokens_from_cookies(file_path):
    cookies = load_lines(file_path)
    tokens = []
    count = 0
    for i, cookie in enumerate(cookies, start=1):
        token = get_token_from_cookie(cookie)
        if token:
            print(f"✅ Cookie {i} converted to token")
            tokens.append(token)
            count += 1
        else:
            print(f"❌ Cookie {i} failed")
    print(f"🟢 {count} cookies converted successfully")
    return tokens

def main():
    check_password()
    print_logo()

    mode = input("🔰 Mode [single/multi]: ").lower()
    login_type = input("🔑 Login using [token/cookie]: ").lower()

    tokens = []

    if login_type == "cookie":
        file_path = input("📄 Cookie file path: ")
        tokens = load_tokens_from_cookies(file_path)
    else:
        if mode == "multi":
            path = input("📂 Enter token file path: ")
            tokens = load_lines(path)
        else:
            tokens = [input("🔐 Enter Facebook Token: ")]

    if not tokens:
        print("❌ No valid tokens loaded. Exiting.")
        return

    print("\n👤 ID Info:")
    for t in tokens:
        name = get_user_name(t)
        print(f"✅ {name} loaded")

    backup_path = input("🔧 Enter backup token file path (or leave blank): ").strip()
    backup_tokens = load_lines(backup_path) if backup_path else []

    use_pages = input("📣 Use pages for commenting? (y/n): ").lower() == 'y'
    if use_pages:
        new_tokens = []
        for t in tokens:
            pages = get_page_list(t)
            for name, p in pages.items():
                print(f"📘 Page Loaded: {name}")
                new_tokens.append(p["token"])
        tokens = new_tokens

    post_mode = input("📌 Post mode [wall/manual]: ").lower()
    post_ids = []

    if post_mode == 'wall':
        limit = int(input("🔢 Posts per ID: "))
        for t in tokens:
            ids = get_post_ids_from_wall(t, limit)
            if not ids:
                print("⚠️ Skipping this ID (wall not loaded)")
                continue
            post_ids.extend(ids)
    else:
        post_ids = input("📝 Enter post IDs (comma-separated): ").split(',')

    hatters = []
    if input("🚫 Add hatter list? (y/n): ").lower() == 'y':
        hatters = input("❌ Enter hatter post IDs (comma-separated): ").split(',')

    comment_file = input("💬 Enter comment file (leave blank for manual input): ").strip()
    if comment_file:
        comments = load_lines(comment_file)
    else:
        comments = [input("💬 Enter your comment: ")]

    delay = int(input("⏱️ Delay between comments (in seconds): "))
    print("\n🚀 Starting Auto Comment...\n")

    total_success = 0
    for token in tokens:
        for post_id in post_ids:
            post_id = post_id.strip()
            if post_id in hatters:
                print(f"⛔ Skipped hatter post: {post_id}")
                continue
            comment = random.choice(comments)
            res = comment_post(token, post_id, comment)
            if "id" in res:
                print(f"✅ Comment Sent → Post: {post_id} | Comment: {comment}")
                total_success += 1
            else:
                err = res.get("error", {}).get("message", "Unknown error")
                print(f"⚠️ Failed → Post: {post_id} | Error: {err}")
                # Try backup token
                for backup in backup_tokens:
                    res_bk = comment_post(backup, post_id, comment)
                    if "id" in res_bk:
                        print(f"🔁 Backup Used → Post: {post_id} | Comment: {comment}")
                        total_success += 1
                        break
            time.sleep(delay)

    print(f"\n✅ Done! Total comments sent: {total_success}")

if __name__ == "__main__":
    main()
