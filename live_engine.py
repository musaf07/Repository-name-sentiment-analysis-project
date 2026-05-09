from reddit_fetch import fetch_reddit_posts
from youtube_fetch import fetch_youtube_comments
from trends import get_trend_score

def collect_live_data(product):

    reddit = fetch_reddit_posts(product)

    youtube = fetch_youtube_comments(product)

    trend = get_trend_score(product)

    return {

        "posts":
        reddit + youtube,

        "trend_score":
        trend
    }