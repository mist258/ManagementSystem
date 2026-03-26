from enum import StrEnum


class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"


class ArticleSortField(StrEnum):
    created_at = "created_at"
    title = "title"
