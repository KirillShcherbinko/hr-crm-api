from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID


class IVacancyCandidateRepository(ABC):
    @abstractmethod
    async def list_by_vacancy(self,
                              vacancy_id: UUID) -> List[Dict[str,
                                                             Any]]: ...

    @abstractmethod
    async def assign(self,
                     vacancy_id: UUID,
                     candidate_id: UUID,
                     assigned_by: UUID) -> Dict[str,
                                                Any]: ...

    @abstractmethod
    async def unassign(self, vacancy_id: UUID, candidate_id: UUID) -> None: ...

    @abstractmethod
    async def move_stage(self,
                         vacancy_candidate_id: UUID,
                         new_stage_id: UUID,
                         moved_by: UUID) -> Dict[str,
                                                 Any]: ...

    @abstractmethod
    async def get_transitions(self,
                              vacancy_candidate_id: UUID) -> List[Dict[str,
                                                                       Any]]: ...
