import pandas as pd
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def extract_endpoint(endpoint):
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        timeout=(10, 30),
    )
    response.raise_for_status()

    data = response.json()

    if (
        not isinstance(data, list)
        or not data
        or not all(isinstance(record, dict) for record in data)
    ):
        raise ValueError(f"Unexpected response from {endpoint}")

    df = pd.DataFrame(data)
    print(f"Extracted {len(df)} {endpoint}")
    return df


def extract_posts():
    return extract_endpoint("posts")


def extract_comments():
    return extract_endpoint("comments")