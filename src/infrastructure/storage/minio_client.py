from minio import Minio
from minio.error import S3Error
from src.config.settings import settings


def get_minio_client() -> Minio:
    client = Minio(
        "minio:9000",
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False
    )

    bucket_name = "resumes"
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except S3Error as e:
        if e.code != "BucketAlreadyOwnedByYou":
            raise

    return client
