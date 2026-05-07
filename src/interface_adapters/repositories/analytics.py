from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID


class IAnalyticsRepository(ABC):
    @abstractmethod
    async def get_vacancy_stats(self, vacancy_id: UUID) -> Dict[str, Any]: ...
    @abstractmethod
    async def get_recruiter_load(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_recruiter_stats(self,
                                  recruiter_id: UUID) -> Dict[str,
                                                              Any]: ...

    @abstractmethod
    async def get_summary(self) -> Dict[str, Any]: ...
