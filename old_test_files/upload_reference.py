import os
import requests

API_URL = "http://127.0.0.1:8000/api/reference-images/"

IMAGE_PATH = os.path.expanduser(
    r"~/Downloads/cute krishna.jpg"
)

token = input("Paste your Supabase access token: ").strip()

if not os.path.exists(IMAGE_PATH):
    print("Image not found:")
    print(IMAGE_PATH)
    raise SystemExit

print("Image found:")
print(IMAGE_PATH)

headers = {
    "Authorization": f"Bearer {token}"
}

with open(IMAGE_PATH, "rb") as image_file:

    data = {
        "image_url": "http://127.0.0.1:8000/media/profile_pictures/cute_krishna.jpg"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        data=data
    )

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)