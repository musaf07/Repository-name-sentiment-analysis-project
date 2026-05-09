from googleapiclient.discovery import build

API_KEY = "YOUR_YOUTUBE_API_KEY"

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

def fetch_youtube_comments(keyword):

    comments = []

    req = youtube.search().list(
        q=keyword,
        part="snippet",
        maxResults=5
    )

    res = req.execute()

    for item in res["items"]:

        comments.append({

            "platform": "YouTube",

            "text":
            item["snippet"]["title"]
        })

    return comments