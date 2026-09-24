import requests

PROJECT_ID = 2

API_URL = f"http://127.0.0.1:8000/api/projects/{PROJECT_ID}/regenerate/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    API_URL,
    headers=headers,
    json={}
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)