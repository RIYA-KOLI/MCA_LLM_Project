import requests


BASE_URL = "https://hacker-news.firebaseio.com/v0"


def get_top_story_ids():

    url = f"{BASE_URL}/topstories.json"

    return requests.get(url).json()


def get_story(story_id):

    url = f"{BASE_URL}/item/{story_id}.json"

    return requests.get(url).json()


def get_top_stories(limit=15):

    ids = get_top_story_ids()

    stories = []

    for story_id in ids[:limit]:

        story = get_story(story_id)

        if story:
            stories.append(story)

    return stories