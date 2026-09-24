import requests

BASE_URL = "http://127.0.0.1:8000"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}"
}

data = {
    "project": 3,
    "file_url": "http://127.0.0.1:8000/media/regenerated_project_3_generation_1.jpg",
    "file_type": "jpg"
}

response = requests.post(
    f"{BASE_URL}/api/exports/",
    headers=headers,
    data=data
)

print("\nSTATUS:", response.status_code)

print("\nRESPONSE:")
print(response.text)