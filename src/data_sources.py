import random

def get_tweets(keyword="product"):

    sample_data = [
        "Amazing product!",
        "Worst service ever",
        "Good quality",
        "Not satisfied",
        "Excellent experience",
        "Bad delivery",
        "Loved it!",
        "Average performance",
        "Very happy with this",
        "Terrible support"
    ]

    # simulate live tweets
    return random.sample(sample_data, 6)