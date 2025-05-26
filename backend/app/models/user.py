from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
import uuid

from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.item import Item


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, min_length=3, max_length=255)
    full_name: Optional[str] = Field(
        default=None, min_length=1, max_length=255)
    is_active: bool = True
    role: UserRole = Field(default=UserRole.user)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    items: List["Item"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)
    role: Optional[UserRole] = UserRole.user


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, min_length=3, max_length=255)
    full_name: Optional[str] = Field(
        default=None, min_length=1, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=100)
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserPublicWithItems(UserPublic):
    items: List["ItemPublic"] = []


# Resolve forward references
from app.models.item import ItemPublic  # noqa: E402
UserPublicWithItems.model_rebuild()
