import requests

API_URL = "http://127.0.0.1:8000/api/projects/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

project_data = {
    "name": "Krishna Style Project",

    "original_image_url": "http://127.0.0.1:8000/media/profile_pictures/cute_krishna.jpg",

    "edited_image_url": "",

    "editing_profile": 5
}

response = requests.post(
    API_URL,
    headers=headers,
    json=project_data
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)