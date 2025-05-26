from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
import uuid

from sqlmodel import Field, SQLModel, Relationship
from pydantic import field_validator

from app.models.enums import ItemStatus, ItemCategory

if TYPE_CHECKING:
    from app.models.user import User


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(ge=0, le=1000000)
    quantity: int = Field(default=1, ge=0, le=10000)
    category: ItemCategory = Field(default=ItemCategory.other)
    status: ItemStatus = Field(default=ItemStatus.draft)
    is_available: bool = True

    @field_validator('price')
    @classmethod
    def price_must_have_two_decimals(cls, v: float) -> float:
        return round(v, 2)


class Item(ItemBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    owner: Optional["User"] = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: Optional[float] = Field(default=None, ge=0, le=1000000)
    quantity: Optional[int] = Field(default=None, ge=0, le=10000)
    category: Optional[ItemCategory] = None
    status: Optional[ItemStatus] = None
    is_available: Optional[bool] = None

    @field_validator('price')
    @classmethod
    def price_must_have_two_decimals(cls, v: Optional[float]) -> Optional[float]:
        return round(v, 2) if v is not None else None


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ItemPublicWithOwner(ItemPublic):
    owner: Optional["UserPublic"] = None


# Resolve forward references
from app.models.user import UserPublic  # noqa: E402
ItemPublicWithOwner.model_rebuild()
