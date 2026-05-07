from typing import Dict, Any
from uuid import UUID
from minio import Minio
from src.interface_adapters.repositories.candidate import ICandidateRepository


class DetachResumeUseCase:
    def __init__(self, candidate_repo: ICandidateRepository,
                 minio_client: Minio):
        self.candidate_repo = candidate_repo
        self.minio_client = minio_client
        self.bucket = "resumes"

    async def execute(self, candidate_id: UUID) -> Dict[str, Any]:
        candidate = await self.candidate_repo.get_by_id(candidate_id)
        if candidate and candidate.get("resume_url"):
            try:
                path = candidate["resume_url"].replace(
                    f"minio://{self.bucket}/", "")
                self.minio_client.remove_object(self.bucket, path)
            except Exception:
                pass
        return await self.candidate_repo.detach_resume(candidate_id)
