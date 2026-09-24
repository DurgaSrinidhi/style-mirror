import requests

BASE_URL = "http://127.0.0.1:8000"

# Your Supabase access token must already be stored in $token
token = input("Paste your Supabase access token: ").strip()

image_path = r"C:\Users\DELL\Downloads\cute krishna.jpg"

headers = {
    "Authorization": f"Bearer {token}"
}

with open(image_path, "rb") as image_file:

    files = {
        "image": (
            "cute_krishna.jpg",
            image_file,
            "image/jpeg"
        )
    }

    response = requests.post(
        f"{BASE_URL}/api/generate-style-profile/",
        headers=headers,
        files=files
    )

print("\nSTATUS:", response.status_code)
print("\nRESPONSE:")
print(response.text)