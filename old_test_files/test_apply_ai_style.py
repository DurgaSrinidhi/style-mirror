import requests

BASE_URL = "http://127.0.0.1:8000"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}"
}

data = {
    "project_id": 3,
    "profile_id": 6
}

response = requests.post(
    f"{BASE_URL}/api/apply-style/",
    headers=headers,
    data=data
)

print("\nSTATUS:", response.status_code)

print("\nRESPONSE:")
print(response.text)