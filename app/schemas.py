from pydantic import BaseModel,HttpUrl
from typing import Optional


class URLCreate(BaseModel):
    url: HttpUrl
    ttl: Optional[int] = None
    #요청을 받는 용도라 from_attributes(orm_mode) 없음

