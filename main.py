import charset_normalizer.md
import praw
from praw.models import MoreComments


# helper that determines if a number is contained within any string
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


# helepr that determines if a string contains any symbols
def has_symbols(inputString):
    inputString.replace(" ", "")
    return any(not char.isalnum() for char in inputString)


# authenticate
reddit = praw.Reddit(client_id='D2eF3b3l9xL5g6P61ziPrw', client_secret='smvmphUJ1a2-Pce-0dlloZ7Bk0PDNQ',
                     user_agent='WSB Webscraper')

# set up vars
hot_posts = reddit.subreddit('WallStreetBets').top(time_filter="day", limit=50)

ticketers_dict = {}

# parse the post and check for any ticketers
for post in hot_posts:
    # scrape post titles for ticketers
    if '$' in post.title:
        submission_post_title = post.title.split('$', 1)[1].split(" ", 1)[0]
        if not has_numbers(submission_post_title) and not has_symbols(submission_post_title):
            ticketers_dict.update({submission_post_title: ticketers_dict.get(submission_post_title, 0) + 1})

    # scrape each post's comment section for ticketers
    post.comments.replace_more(limit=0)
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue

        if '$' in comment.body:
            comment_body_text = comment.body.split('$', 1)[1].split(" ", 1)[0]
            if not has_numbers(comment_body_text) and not has_symbols(comment_body_text):
                ticketers_dict.update({comment_body_text: ticketers_dict.get(comment_body_text, 0) + 1})

print(ticketers_dict)
print("The top ticket to buy puts on today is $", max(ticketers_dict, key=ticketers_dict.get))
