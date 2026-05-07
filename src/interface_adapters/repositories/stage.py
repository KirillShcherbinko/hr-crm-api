from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID


class IVacancyStageRepository(ABC):
    @abstractmethod
    async def list_by_vacancy(self,
                              vacancy_id: UUID) -> List[Dict[str,
                                                             Any]]: ...

    @abstractmethod
    async def create(self,
                     vacancy_id: UUID,
                     stage_data: Dict[str,
                                      Any]) -> Dict[str,
                                                    Any]: ...

    @abstractmethod
    async def update(self,
                     stage_id: UUID,
                     stage_data: Dict[str,
                                      Any]) -> Dict[str,
                                                    Any]: ...

    @abstractmethod
    async def delete(self, stage_id: UUID) -> None: ...

    @abstractmethod
    async def reorder(self,
                      vacancy_id: UUID,
                      new_order: List[UUID]) -> List[Dict[str,
                                                          Any]]: ...
