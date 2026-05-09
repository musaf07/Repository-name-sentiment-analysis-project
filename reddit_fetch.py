import praw

reddit = praw.Reddit(

    client_id="YOUR_CLIENT_ID",

    client_secret="YOUR_SECRET",

    user_agent="sentiment_app"
)

def fetch_reddit_posts(keyword):

    posts = []

    subreddit = reddit.subreddit("all")

    for post in subreddit.search(
        keyword,
        limit=10
    ):

        posts.append({

            "platform": "Reddit",

            "text": post.title
        })

    return posts