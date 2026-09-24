import requests

BASE_URL = "http://127.0.0.1:8000"

token = input("Paste your Supabase access token: ").strip()

image_path = r"C:\Users\DELL\Downloads\cute krishna.jpg"

headers = {
    "Authorization": f"Bearer {token}"
}

with open(image_path, "rb") as image_file:

    files = {
        "image": (
            "original.jpg",
            image_file,
            "image/jpeg"
        )
    }

    data = {
        "image_type": "original"
    }

    response = requests.post(
        f"{BASE_URL}/api/uploaded-images/",
        headers=headers,
        files=files,
        data=data
    )

print("\nSTATUS:", response.status_code)
print("\nRESPONSE:")
print(response.text)