import requests

BASE_URL = "http://127.0.0.1:8000"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}"
}

data = {
    "name": "AI Style Mirror Test Project",
    "original_image_url": "http://127.0.0.1:8000/media/uploads/original.jpg",
    "editing_profile": 6
}

response = requests.post(
    f"{BASE_URL}/api/projects/",
    headers=headers,
    data=data
)

print("\nSTATUS:", response.status_code)

print("\nRESPONSE:")
print(response.text)