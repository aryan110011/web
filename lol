import time
import json
import requests
from datetime import datetime

# Password Protection
def password_protection():
    password = "your_secure_password"  # Replace with your secure password
    entered_password = input("🔒 Enter password to access the tool: ")
    if entered_password != password:
        print("❌ Incorrect password. Exiting...")
        exit()

# Logo with red color
def print_logo():
    start_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    print("\n\n")  # To make space before logo
    print("\033[91m" + r""" 
   ███████╗██████╗ ██╗     ██╗███╗   ██╗██╗     ██╗     ███████╗
   ██╔════╝██╔══██╗██║     ██║████╗  ██║██║     ██║     ██╔════╝
   █████╗  ██████╔╝██║     ██║██╔██╗ ██║██║     ██║     █████╗  
   ██╔══╝  ██╔══██╗██║     ██║██║╚██╗██║██║     ██║     ██╔══╝  
   ███████╗██║  ██║██████╗ ██║██║ ╚████║██████╗ ██║     ███████╗
   ╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝     ╚══════╝
                                                                 
   """ + "\033[0m")  # Reset color back to normal
    print(f"🕒 Tool Started At: {start_time}\n")

# Function to comment on a post using the token
def comment_on_post(token, post_id, comment):
    # Placeholder for the actual Facebook API call to post comment
    print(f"📌 Comment sent from {token} to Post ID {post_id}: {comment}")

# Function to comment on a page using the token
def comment_on_page(token, page_id, comment):
    # Placeholder for the actual Facebook API call to post comment on page
    print(f"📌 Comment sent from {token} to Page ID {page_id}: {comment}")

# Function to perform commenting on both posts and pages
def comment_on_post_or_page(tokens, post_id_or_page_id, comment, delay, is_page=False):
    for token in tokens:
        if is_page:
            comment_on_page(token, post_id_or_page_id, comment)
            print(f"🌟 Comment sent from Token: {token} to Page: {post_id_or_page_id}")
        else:
            comment_on_post(token, post_id_or_page_id, comment)
            print(f"🌟 Comment sent from Token: {token} to Post ID: {post_id_or_page_id}")
        time.sleep(delay)

# Main function to run the script
def main():
    password_protection()  # Enforce password protection

    print_logo()  # Display logo

    # Prompt user for mode (single/multi) and login type (token/cookie)
    mode = input("🔄 Choose mode (single/multi): ").lower()
    login_type = input("🔑 Login using (token/cookie): ").lower()

    # Load tokens based on mode
    tokens = []
    if login_type == "cookie":
        if mode == "multi":
            file_path = input("📂 Cookie file path: ")
            tokens = load_tokens_from_cookies(file_path)
        else:
            cookie = input("🍪 Enter single cookie: ")
            token = get_token_from_cookie(cookie)
            tokens.append(token)
            print(f"✅ Cookie converted to token: {token}")
    elif login_type == "token":
        token = input("🔑 Enter token: ")
        tokens.append(token)
        print(f"✅ Token added: {token}")

    # Ask user if they want to comment on a page or post
    is_page = input("💡 Comment on Page (yes/no)? ").lower() == "yes"

    # Get post ID or page ID
    post_id_or_page_id = input("🔗 Enter Post/Page ID to comment on: ")

    # Get the comment
    comment = input("💬 Enter your comment: ")

    # Ask for delay
    delay = int(input("⏳ Set delay between comments (seconds): "))

    # Start commenting
    comment_on_post_or_page(tokens, post_id_or_page_id, comment, delay, is_page)

    print("\n✅ Tool execution completed successfully!")

if __name__ == "__main__":
    main()
