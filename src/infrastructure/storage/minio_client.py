from minio import Minio
from src.config.settings import settings


def get_minio_client() -> Minio:
    return Minio(
        "minio:9000",
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False
    )
