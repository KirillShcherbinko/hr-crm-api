from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID


class IEmailRepository(ABC):
    @abstractmethod
    async def send(self,
                   email_data: Dict[str,
                                    Any],
                   sent_by: UUID) -> Dict[str,
                                          Any]: ...

    @abstractmethod
    async def list(self,
                   filters: Dict[str,
                                 Any],
                   skip: int = 0,
                   limit: int = 50) -> List[Dict[str,
                                                 Any]]: ...

    @abstractmethod
    async def get_by_id(self, email_id: UUID) -> Optional[Dict[str, Any]]: ...
