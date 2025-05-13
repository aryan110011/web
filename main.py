import requests
import time
import random
import json
import os
from browser_cookie3 import chrome

# ---------- PASSWORD PROTECTION ----------
PASSWORD = "aryan123"  # 👈 Yahan apna password rakh le

def check_password():
    user_pass = input("🔒 Enter Script Password: ")
    if user_pass != PASSWORD:
        print("❌ Wrong password! Access denied.")
        exit()

# ---------- LOGO ----------
logo = """
█████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║
███████║██████╔╝██║   ██║███████║██╔██╗ ██║
██╔══██║██╔═══╝ ██║   ██║██╔══██║██║╚██╗██║
██║  ██║██║     ╚██████╔╝██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
     🔥 Facebook Auto Comment Tool by Aryan 🔥
"""

# ---------- COOKIE FUNCTION ----------
def get_facebook_cookies():
    try:
        cj = chrome(domain_name="facebook.com")
        cookies = {}
        for cookie in cj:
            cookies[cookie.name] = cookie.value
        return cookies
    except Exception as e:
        print("❌ Failed to fetch cookies:", e)
        return None

# ---------- PAGE LIST FUNCTION ----------
def get_page_list(token):
    url = f"https://graph.facebook.com/me/accounts?access_token={token}"
    res = requests.get(url).json()
    pages = {}
    if "data" in res:
        for page in res['data']:
            pages[page['name']] = {
                'id': page['id'],
                'token': page['access_token']
            }
    return pages

# ---------- POST LOADER FUNCTION ----------
def get_post_ids_from_wall(token, limit=10):
    url = f"https://graph.facebook.com/me/feed?limit={limit}&access_token={token}"
    res = requests.get(url).json()
    post_ids = []
    if "data" in res:
        for post in res["data"]:
            post_ids.append(post["id"])
    return post_ids

# ---------- COMMENT FUNCTION ----------
def comment_post(token, post_id, message):
    url = f"https://graph.facebook.com/{post_id}/comments"
    data = {
        'message': message,
        'access_token': token
    }
    res = requests.post(url, data=data).json()
    return res

# ---------- TOKEN LOADER FUNCTION ----------
def load_tokens(file_path):
    if not os.path.exists(file_path):
        print("❌ Token file not found!")
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# ---------- MAIN FUNCTION ----------
def main():
    check_password()  # 👈 First check for password
    print(logo)

    mode = input("🎯 Mode [single/multi]: ").lower()
    login_type = input("🔐 Login via [token/cookie]: ").lower()

    if login_type == "token":
        if mode == "multi":
            token_file = input("📄 Enter token file path: ")
            tokens = load_tokens(token_file)
        else:
            token = input("🔑 Enter your Facebook token: ")
            tokens = [token]
    else:
        cookies = get_facebook_cookies()
        print("✅ Cookie fetched. (Note: Not used in comment logic yet)")
        return

    use_pages = input("📣 Comment using Page? (y/n): ").lower() == 'y'
    page_tokens = []
    if use_pages:
        for t in tokens:
            pages = get_page_list(t)
            for name, info in pages.items():
                print(f"📝 Page: {name}")
                page_tokens.append(info['token'])
        tokens = page_tokens

    post_mode = input("📌 Load posts from wall? (y/n): ").lower()
    if post_mode == 'y':
        limit = int(input("🔢 How many posts to load?: "))
        post_ids = []
        for t in tokens:
            post_ids += get_post_ids_from_wall(t, limit)
    else:
        post_ids = input("🧾 Enter post IDs (comma-separated): ").split(',')

    hatter_list_input = input("🚫 Enter hatter post IDs (comma-separated or blank): ").strip()
    hatter_list = [h.strip() for h in hatter_list_input.split(',')] if hatter_list_input else []

    comment_path = input("📝 Path to comment file or leave blank for manual input: ")
    if comment_path and os.path.exists(comment_path):
        with open(comment_path, 'r') as f:
            comments = [line.strip() for line in f if line.strip()]
    else:
        comments = [input("💬 Enter comment: ")]

    delay = int(input("⏱️ Delay between comments (in seconds): "))
    print("\n🚀 Starting auto-commenter...\n")

    for token in tokens:
        for post_id in post_ids:
            post_id = post_id.strip()
            if post_id in hatter_list:
                print(f"⛔ Skipping hatter post {post_id}")
                continue
            comment = random.choice(comments)
            try:
                res = comment_post(token, post_id, comment)
                if "id" in res:
                    print(f"✅ Commented on {post_id} → Comment ID: {res['id']}")
                else:
                    print(f"❌ Failed on {post_id} → {res}")
            except Exception as e:
                print(f"❌ Error on {post_id}: {e}")
            time.sleep(delay)

# ---------- RUN SCRIPT ----------
if __name__ == "__main__":
    main()
