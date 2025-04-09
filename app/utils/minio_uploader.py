import base64
import uuid
from minio import Minio
from minio.error import S3Error
from io import BytesIO

client = Minio(
    "localhost:9000",  # или твой хост
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET_NAME = "post-images"

def upload_base64_image(base64_data: str) -> str:
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    image_data = base64.b64decode(base64_data)
    image_id = str(uuid.uuid4()) + ".png"
    image_io = BytesIO(image_data)

    client.put_object(
        BUCKET_NAME,
        image_id,
        image_io,
        length=len(image_data),
        content_type="image/png"
    )

    return f"http://localhost:9000/{BUCKET_NAME}/{image_id}"
