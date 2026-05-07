from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID


class ICandidateRepository(ABC):
    @abstractmethod
    async def create(self,
                     candidate_data: Dict[str,
                                          Any],
                     created_by: UUID) -> Dict[str,
                                               Any]: ...

    @abstractmethod
    async def get_by_id(self,
                        candidate_id: UUID) -> Optional[Dict[str,
                                                             Any]]: ...

    @abstractmethod
    async def list(self,
                   filters: Dict[str,
                                 Any],
                   skip: int = 0,
                   limit: int = 50) -> List[Dict[str,
                                                 Any]]: ...

    @abstractmethod
    async def update(self,
                     candidate_id: UUID,
                     candidate_data: Dict[str,
                                          Any]) -> Dict[str,
                                                        Any]: ...

    @abstractmethod
    async def delete(self, candidate_id: UUID) -> None: ...

    @abstractmethod
    async def attach_resume(self,
                            candidate_id: UUID,
                            file_url: str) -> Dict[str,
                                                   Any]: ...

    @abstractmethod
    async def detach_resume(self, candidate_id: UUID) -> Dict[str, Any]: ...

    @abstractmethod
    async def get_emails_history(self,
                                 candidate_id: UUID) -> List[Dict[str,
                                                                  Any]]: ...
