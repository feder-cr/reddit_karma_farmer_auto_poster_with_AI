import re
from config_secrets import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, OPENAI_API_KEY
import praw
from time import sleep
from random import randint, shuffle
import time
from generator_post import GeneratorPostGPT
from praw.exceptions import RedditAPIException
import warnings
import re
warnings.filterwarnings("ignore")

reddit = praw.Reddit(
client_id=REDDIT_CLIENT_ID,
client_secret=REDDIT_CLIENT_SECRET,
username=REDDIT_USERNAME,
password=REDDIT_PASSWORD,
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

def clean_text(text: str) -> str:
    text = text.replace('Title:', '').replace('Body:', '').replace('"', '').replace('*', '').strip()
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def has_posted_recently(subreddit_name: str) -> bool:
    current_time = time.time()
    try:
        user_posts = reddit.user.me().submissions.new(limit=1000)
        for submission in user_posts:
            if submission.subreddit.display_name == subreddit_name and current_time - submission.created_utc < 86400:
                return True
    except RedditAPIException as e:
        print(f"An error occurred while checking recent posts: {e}")
    return False

def extract_title_body(response):
    title_match = re.search(r'Title:\s*"(.*?)"\s*\n{2}', response, re.DOTALL)
    body_match = re.search(r'Body:\s*"(.*?)"', response, re.DOTALL)
    title = title_match.group(1) if title_match else None
    body = body_match.group(1) if body_match else None
    return title, body

def can_post_to_subreddit(subreddit_name: str) -> bool:
    try:         
        test_submission = reddit.subreddit(subreddit_name).submit("Test PostTest PostTest PostTest PostTest PostTest PostTest Post", selftext="This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.This is a test to check if posting is allowed.")
        test_submission.delete()
        return True
    except RedditAPIException as e:
        if e.error_type in ["SUBREDDIT_NOTALLOWED", "SUBREDDIT_NOTALLOWED_BANNED"]:
            print(f"Cannot post in r/{subreddit_name} - possibly banned or restricted.")
        else:
            print(f"An error occurred while checking if posting is allowed in r/{subreddit_name}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while checking if posting is allowed in r/{subreddit_name}: {e}")
        return False

def try_post(subreddit_name: str, title: str, body: str) -> bool:
    try:
        submission = reddit.subreddit(subreddit_name).submit(title.strip(), selftext=body.strip())
        post_url = submission.url
        print(f"Post published in r/{subreddit_name}: {post_url}")
        with open("posted_links.txt", "a") as file:
            file.write(f"{post_url}\n")
        if randint(1, 40) == 1:
            sleep(randint(100, 5000))
        else:
            sleep(randint(10, 1000))
        return True
    except RedditAPIException as e:
        if e.error_type == "RATELIMIT":
            sleep(int(e.message.split(" ")[-5]) * 60)
        elif e.error_type in ["SUBREDDIT_NOTALLOWED", "SUBREDDIT_NOTALLOWED_BANNED"]:
            print(f"Cannot post in r/{subreddit_name} - possibly banned or restricted.")
        else:
            print(f"An error occurred while posting to r/{subreddit_name}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while posting to r/{subreddit_name}: {e}")
        return False

def get_subreddit_rules(subreddit_name: str) -> str:
    try:
        rules = reddit.subreddit(subreddit_name).rules()
        return str(rules)
    except Exception as e:
        print(f"An error occurred while fetching rules for r/{subreddit_name}: {e}")
        return ""
 

def main():
    trending_subreddits = list(reddit.subreddits.popular(limit=5000))
    shuffle(trending_subreddits)
    generator_post = GeneratorPostGPT(openai_api_key=OPENAI_API_KEY)
    for subreddit in trending_subreddits:
        source_subreddit = subreddit.display_name
        print(f"Processing subreddit: {source_subreddit}")
        if has_posted_recently(source_subreddit):
            print(f"Skipping subreddit {source_subreddit} because a post was made in the last 24 hours.")
            continue
        if not can_post_to_subreddit(source_subreddit):
            print(f"Skipping subreddit {source_subreddit} because we are not allowed to post.")
            continue
        try:
            top_posts = reddit.subreddit(source_subreddit).top("day", limit=10)
            post_titles = "\n".join([f"- {post.title}" for post in top_posts])
            subreddit_rules = get_subreddit_rules(source_subreddit)
            innovative_post = generator_post.generate_post(source_subreddit, post_titles, rules=subreddit_rules)
            if innovative_post:
                try:
                    title, body = extract_title_body(innovative_post)
                    title = clean_text(title)
                    body = clean_text(body)
                    if title and body:
                        if not try_post(source_subreddit, title, body):
                            print(f"Failed to post in r/{source_subreddit}. Skipping.")
                            continue
                    else:
                        print(f"Generated post for r/{source_subreddit} is empty. Skipping.")
                        continue
                except ValueError:
                    print(f"Invalid post format for r/{source_subreddit}. Skipping.")
                    continue
                except Exception:
                    print(f"Invalid post format for r/{source_subreddit}. Skipping.")
                    continue
            else:
                print(f"Failed to generate post for r/{source_subreddit}. Skipping.")
                continue
        except RedditAPIException as e:
            if e.error_type == "RATELIMIT":
                sleep(int(e.message.split(" ")[-5]) * 60)
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Skipping subreddit r/{source_subreddit}.")
            continue

if __name__ == "__main__":
    main()