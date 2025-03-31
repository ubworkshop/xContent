import tweepy
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, scrolledtext
import markdown

# Twitter API 配置 (需要你自己申请API密钥)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# 初始化Twitter API
def setup_twitter_api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

# 获取最近一周推文并转换为Markdown
def get_user_tweets(username):
    try:
        api = setup_twitter_api()
        # 计算一周前的时间
        one_week_ago = datetime.now() - timedelta(days=7)
        
        # 获取用户推文 (最多200条，可调整count参数)
        tweets = api.user_timeline(
            screen_name=username,
            count=200,
            tweet_mode="extended"
        )
        
        # 过滤最近一周的推文并转换为Markdown
        markdown_output = f"# @{username} 最近一周的推文\n\n"
        for tweet in tweets:
            tweet_time = tweet.created_at
            if tweet_time >= one_week_ago:
                tweet_text = tweet.full_text
                tweet_date = tweet_time.strftime("%Y-%m-%d %H:%M:%S")
                markdown_output += f"## 发表于 {tweet_date}\n\n{tweet_text}\n\n---\n"
        
        return markdown_output if markdown_output != f"# @{username} 最近一周的推文\n\n" else f"# @{username} 最近一周的推文\n\n该用户本周没有发文。"
    except Exception as e:
        return f"发生错误: {str(e)}"

# GUI界面和运行按钮
def create_gui():
    window = tk.Tk()
    window.title("Twitter推文获取工具")
    window.geometry("600x400")

    # 用户名输入框
    tk.Label(window, text="请输入Twitter用户名:").pack(pady=5)
    username_entry = tk.Entry(window, width=30)
    username_entry.pack(pady=5)

    # 输出区域
    output_text = scrolledtext.ScrolledText(window, width=70, height=20)
    output_text.pack(pady=10)

    # 运行按钮功能
    def run_script():
        username = username_entry.get().strip()
        if username:
            result = get_user_tweets(username)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "请先输入Twitter用户名！")

    # 运行按钮
    run_button = ttk.Button(window, text="运行", command=run_script)
    run_button.pack(pady=5)

    window.mainloop()

# 主程序入口
if __name__ == "__main__":
    create_gui()