from typing import Any, Optional

from pydantic import BaseConfig, BaseModel, Extra


class Base(BaseModel):
    api: Optional[Any]

    class Config(BaseConfig):
        anystr_strip_whitespace = True
        extra = Extra.allow
        use_enum_values = True


class Response(Base):
    request: Optional['Request']


class Request(Base):
    __returning__ = Response

    def url(self, base: str) -> str:
        raise NotImplementedError

    def do(self, api=None) -> __returning__:
        api = api or self.api
        return api.request(self)

    async def do_async(self, api=None) -> __returning__:
        api = api or self.api
        return await api.request(self)


Response.update_forward_refs()
