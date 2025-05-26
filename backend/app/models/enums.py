from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class ItemStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class ItemCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"
    other = "other"
