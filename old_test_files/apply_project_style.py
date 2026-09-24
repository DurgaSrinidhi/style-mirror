import requests

API_URL = "http://127.0.0.1:8000/api/apply-style/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "project_id": 2,
    "profile_id": 5
}

response = requests.post(
    API_URL,
    headers=headers,
    json=data
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)