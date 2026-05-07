from typing import Dict, Any
from uuid import UUID
from io import BytesIO
from minio import Minio
from src.interface_adapters.repositories.candidate import ICandidateRepository
from src.config.settings import settings


class AttachResumeUseCase:
    def __init__(self, candidate_repo: ICandidateRepository,
                 minio_client: Minio):
        self.candidate_repo = candidate_repo
        self.minio_client = minio_client
        self.bucket = "resumes"

    async def execute(self, candidate_id: UUID, file_name: str,
                      file_bytes: bytes) -> Dict[str, Any]:
        self.minio_client.put_object(
            self.bucket, f"{candidate_id}/{file_name}",
            BytesIO(file_bytes), length=len(file_bytes),
            content_type="application/pdf"
        )
        file_url = f"minio://{self.bucket}/{candidate_id}/{file_name}"
        return await self.candidate_repo.attach_resume(candidate_id, file_url)
