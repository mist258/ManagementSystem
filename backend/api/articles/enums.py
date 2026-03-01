from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class ArticleSortField(str, Enum):
    created_at = "created_at"
    title = "title"