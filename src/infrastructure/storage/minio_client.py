from minio import Minio
from src.config.settings import settings

client = Minio(
    "minio:9000",
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False
)
