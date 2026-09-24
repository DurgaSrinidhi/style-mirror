import requests

API_URL = "http://127.0.0.1:8000/api/exports/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

export_data = {
    "project": 2,
    "file_url": "http://127.0.0.1:8000/media/regenerated_project_2_generation_1.jpg",
    "file_type": "jpg"
}

response = requests.post(
    API_URL,
    headers=headers,
    json=export_data
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)