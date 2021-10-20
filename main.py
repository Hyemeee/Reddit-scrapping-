from flask import Flask, render_template, request
from scrapper import aggregate_subreddits


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template("home.html",subreddits=subreddits)
  

@app.route("/read")
def read():
  selected=[]
  for subreddit in subreddits:
    if subreddit in request.args:
      selected.append(subreddit)
  posts=aggregate_subreddits(selected)
  posts.sort(key=lambda post: post['votes'], reverse=True)
  return render_template("read.html",selected=selected,posts=posts)



app.run(host="0.0.0.0")