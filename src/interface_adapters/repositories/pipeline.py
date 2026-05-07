from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID


class IPipelineTemplateRepository(ABC):
    @abstractmethod
    async def list(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def get_by_id(self,
                        template_id: UUID) -> Optional[Dict[str,
                                                            Any]]: ...

    @abstractmethod
    async def create(self,
                     data: Dict[str,
                                Any],
                     created_by: UUID) -> Dict[str,
                                               Any]: ...

    @abstractmethod
    async def update(self,
                     template_id: UUID,
                     pipline_data: Dict[str,
                                        Any]) -> Dict[str,
                                                      Any]: ...

    @abstractmethod
    async def delete(self, template_id: UUID) -> None: ...

    @abstractmethod
    async def add_stage(self,
                        template_id: UUID,
                        pipeline_data: Dict[str,
                                            Any]) -> Dict[str,
                                                          Any]: ...

    @abstractmethod
    async def update_stage(self,
                           stage_id: UUID,
                           pipeline_data: Dict[str,
                                               Any]) -> Dict[str,
                                                             Any]: ...

    @abstractmethod
    async def delete_stage(self, stage_id: UUID) -> None: ...

    @abstractmethod
    async def apply_to_vacancy(self,
                               template_id: UUID,
                               vacancy_id: UUID) -> List[Dict[str,
                                                              Any]]: ...
