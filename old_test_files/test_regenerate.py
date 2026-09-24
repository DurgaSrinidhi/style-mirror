import requests

BASE_URL = "http://127.0.0.1:8000"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.post(
    f"{BASE_URL}/api/projects/3/regenerate/",
    headers=headers
)

print("\nSTATUS:", response.status_code)

print("\nRESPONSE:")
print(response.text)