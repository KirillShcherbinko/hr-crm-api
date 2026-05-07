from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID


class IVacancyRepository(ABC):
    @abstractmethod
    async def create(self,
                     vacancy_data: Dict[str,
                                        Any],
                     created_by: UUID) -> Dict[str,
                                               Any]: ...

    @abstractmethod
    async def get_by_id(self,
                        vacancy_id: UUID) -> Optional[Dict[str,
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
                     vacancy_id: UUID,
                     vacancy_data: Dict[str,
                                        Any]) -> Dict[str,
                                                      Any]: ...

    @abstractmethod
    async def close(self, vacancy_id: UUID) -> Dict[str, Any]: ...
    @abstractmethod
    async def delete(self, vacancy_id: UUID) -> None: ...
