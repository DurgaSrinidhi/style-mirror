import requests

API_URL = "http://127.0.0.1:8000/api/history/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    API_URL,
    headers=headers
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    import json
    print(json.dumps(response.json(), indent=4))
except Exception:
    print(response.text)