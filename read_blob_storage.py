
from io import BytesIO
from PIL import Image

from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv
import os

load_dotenv()

STORAGE_ACCOUNT = os.getenv('STORAGE_ACCOUNT')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')
BLOB_NAME = os.getenv('BLOB_NAME')


# Authenticate using your Azure CLI login
credential = AzureCliCredential()

# Connect to Azure Blob Storage
blob_service = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=credential
)

# Reference the image
blob_client = blob_service.get_blob_client(
    container=CONTAINER_NAME,
    blob=BLOB_NAME
)

# Download image into memory
image_bytes = blob_client.download_blob().readall()

# Convert bytes into a Pillow image
image = Image.open(BytesIO(image_bytes))

# Display image
image.show()

print("Image successfully loaded from Azure!")
