import requests
import time

JUDGE0_URL = "http://localhost:2358"


def get_languages():

    response = requests.get(
        f"{JUDGE0_URL}/languages"
    )

    return response.json()


def run_code(source_code, language_id):

    response = requests.post(
        f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=false",
        json={
            "source_code": source_code,
            "language_id": language_id
        }
    )

    token = response.json()["token"]

    while True:

        result = requests.get(
            f"{JUDGE0_URL}/submissions/{token}?base64_encoded=false"
        ).json()

        if result["status"]["id"] > 2:
            return result

        time.sleep(1)