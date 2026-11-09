import requests

response = requests.get(
    "http://172.24.172.59:11434/api/tags",
    timeout=30,
)
response.raise_for_status()

for model in response.json()["models"]:
    print(model["name"])