from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    limit: int = Field(10, gt=0, lt=15)
    offset: int = Field(0, ge=0)


PaginationDep = Annotated[Pagination, Depends(Pagination)]