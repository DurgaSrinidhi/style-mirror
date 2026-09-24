import requests

API_URL = "http://127.0.0.1:8000/api/editing-profiles/"

token = input("Paste your Supabase access token: ").strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

profile_data = {
    "name": "Krishna Aesthetic",

    "lightness": 10,
    "contrast": 15,
    "warmth": 8,
    "tint": 2,
    "saturation": 12,

    "curve": {
        "points": [
            [0, 0],
            [64, 55],
            [128, 135],
            [192, 205],
            [255, 255]
        ]
    },

    "hsl": {
        "red": {
            "hue": 0,
            "saturation": 5,
            "lightness": 3
        },
        "orange": {
            "hue": 2,
            "saturation": 8,
            "lightness": 5
        },
        "yellow": {
            "hue": -5,
            "saturation": 5,
            "lightness": 5
        },
        "green": {
            "hue": 0,
            "saturation": -5,
            "lightness": 0
        },
        "blue": {
            "hue": 3,
            "saturation": 10,
            "lightness": 5
        }
    },

    "fade": 5,
    "highlight": -5,
    "shadow": 10,
    "color": 5,
    "hue": 2,
    "vignette": 5,
    "sharpen": 10,
    "grain": 3
}

response = requests.post(
    API_URL,
    headers=headers,
    json=profile_data
)

print("\nStatus code:")
print(response.status_code)

print("\nResponse:")

try:
    print(response.json())
except Exception:
    print(response.text)