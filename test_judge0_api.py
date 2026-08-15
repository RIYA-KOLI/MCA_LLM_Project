# test_judge0.py

import requests

response = requests.post(
    "http://localhost:2358/submissions?base64_encoded=false&wait=true",
    json={
        "source_code": "print('Hello Judge0')",
        "language_id": 71
    }
)

print(response.status_code)
print(response.json())