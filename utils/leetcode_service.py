import requests


def get_leetcode_profile(username):

    url = "https://leetcode.com/graphql"

    query = """
    query userProfile($username: String!) {
    matchedUser(username: $username) {
        username

        profile {
        ranking
        reputation
        }

        submitStatsGlobal {
        acSubmissionNum {
            difficulty
            count
        }
        }
    }
    }
"""

    variables = {
        "username": username
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        },
        headers=headers
    )

    return response.json()