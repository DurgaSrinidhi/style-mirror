import os
import requests


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

API_URL = "http://127.0.0.1:8000/api/users/1/"

IMAGE_PATH = os.path.expanduser(
    r"~/Downloads/cute krishna.jpg"
)


# ---------------------------------------------------------
# ENTER YOUR CURRENT SUPABASE ACCESS TOKEN
# ---------------------------------------------------------

token = input("Paste your Supabase access token: ").strip()


# ---------------------------------------------------------
# CHECK IMAGE
# ---------------------------------------------------------

if not os.path.exists(IMAGE_PATH):

    print("Image not found:")
    print(IMAGE_PATH)
    raise SystemExit


print("Image found:")
print(IMAGE_PATH)


# ---------------------------------------------------------
# UPLOAD
# ---------------------------------------------------------

headers = {
    "Authorization": f"Bearer {token}"
}


with open(IMAGE_PATH, "rb") as image_file:

    files = {
        "profile_picture": (
            "cute krishna.jpg",
            image_file,
            "image/jpeg"
        )
    }

    response = requests.patch(
        API_URL,
        headers=headers,
        files=files
    )


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())

except Exception:
    print(response.text)