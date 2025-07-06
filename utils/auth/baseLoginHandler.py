from abc import ABC, abstractmethod
import httpx

class BaseLoginHandler(ABC):
    @abstractmethod
    async def login(self, client: httpx.AsyncClient) -> httpx.AsyncClient:
        pass
