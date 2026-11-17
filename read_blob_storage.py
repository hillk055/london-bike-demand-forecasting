from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import os

load_dotenv()

STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
BLOB_NAME = os.getenv("BLOB_NAME")

credential = DefaultAzureCredential()

blob_service = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=credential
)

blob_client = blob_service.get_blob_client(
    container=CONTAINER_NAME,
    blob=BLOB_NAME
)

image_bytes = blob_client.download_blob().readall()

image = Image.open(BytesIO(image_bytes))

image.show()

print("Image downloaded successfully!")