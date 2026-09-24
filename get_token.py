import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(".env")

url = os.getenv("SUPABASE_URL")

print("Supabase URL loaded:", url)

key = input("Enter your Supabase publishable key: ")
email = input("Enter your test user email: ")
password = input("Enter your test user password: ")

supabase = create_client(url, key)

response = supabase.auth.sign_in_with_password({
    "email": email,
    "password": password
})

print("\nLogin successful!")
print("\nACCESS TOKEN:")
print(response.session.access_token)

