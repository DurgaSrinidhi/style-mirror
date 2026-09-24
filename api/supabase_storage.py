import os
import uuid
from dotenv import load_dotenv
from supabase import create_client

# Load variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

BUCKET_NAME = "style-mirror"

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not configured.")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not configured.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


def upload_file(local_file_path, folder, filename=None):
    """
    Upload a local file to Supabase Storage
    and return its public URL.
    """

    if filename is None:
        filename = os.path.basename(local_file_path)

    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    storage_path = f"{folder}/{unique_filename}"

    with open(local_file_path, "rb") as file:
        file_data = file.read()

    supabase.storage.from_(BUCKET_NAME).upload(
        storage_path,
        file_data,
        {
            "content-type": "image/jpeg",
            "upsert": "true",
        },
    )

    public_url = supabase.storage.from_(
        BUCKET_NAME
    ).get_public_url(storage_path)

    return public_url


def download_file(storage_path, local_file_path):
    """
    Download a file from Supabase Storage
    to a local temporary file.
    """

    file_data = (
        supabase.storage
        .from_(BUCKET_NAME)
        .download(storage_path)
    )

    with open(local_file_path, "wb") as file:
        file.write(file_data)

    return local_file_path