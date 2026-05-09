import tweepy

# =====================================
# 🚀 X (Twitter) API Bearer Token
# =====================================
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJXC9QEAAAAAMM181XIFpCxFElyFsNAcpAPf49o%3DzrWFiwj1JiMJh51qT77tBomHREOBIB1kHKr0ZcQgs9NNVgqcR3"

# =====================================
# 🔗 CONNECT TO X API
# =====================================
client = tweepy.Client(
    bearer_token=BEARER_TOKEN
)

# =====================================
# 📡 FETCH TWEETS
# =====================================
def fetch_tweets(keyword):

    tweets = client.search_recent_tweets(
        query=keyword,
        max_results=10
    )

    # return tweet text
    if tweets.data:
        return [tweet.text for tweet in tweets.data]

    return []


# =====================================
# 🧪 TEST
# =====================================
if __name__ == "__main__":

    data = fetch_tweets("apple")

    print("\n📡 LIVE X POSTS:\n")

    for tweet in data:
        print("👉", tweet)
        print()