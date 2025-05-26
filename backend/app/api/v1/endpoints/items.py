from typing import Annotated, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, or_

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.item import Item, ItemCreate, ItemPublic, ItemUpdate, ItemPublicWithOwner
from app.models.user import User
from app.models.enums import ItemStatus, ItemCategory, UserRole

router = APIRouter()


@router.post("/", response_model=ItemPublic)
async def create_item(
    item: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    item_dict = item.model_dump()
    item_dict["owner_id"] = current_user.id

    db_item = Item(**item_dict)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[ItemPublicWithOwner])
async def read_items(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    status: Optional[ItemStatus] = None,
    category: Optional[ItemCategory] = None,
    is_available: Optional[bool] = None,
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    search: Optional[str] = None,
):
    statement = select(Item)

    # Apply filters
    if status:
        statement = statement.where(Item.status == status)
    if category:
        statement = statement.where(Item.category == category)
    if is_available is not None:
        statement = statement.where(Item.is_available == is_available)
    if min_price is not None:
        statement = statement.where(Item.price >= min_price)
    if max_price is not None:
        statement = statement.where(Item.price <= max_price)
    if search:
        statement = statement.where(
            or_(
                Item.title.contains(search),
                Item.description.contains(search)
            )
        )

    statement = statement.offset(skip).limit(limit)
    items = db.exec(statement).all()
    return items


@router.get("/my", response_model=List[ItemPublic])
async def read_my_items(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    statement = select(Item).where(
        Item.owner_id == current_user.id).offset(skip).limit(limit)
    items = db.exec(statement).all()
    return items


@router.get("/{item_id}", response_model=ItemPublicWithOwner)
async def read_item(
    item_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ItemPublic)
async def update_item(
    item_id: uuid.UUID,
    item_update: ItemUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check permissions
    if item.owner_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Only owner or admin can change status to published
    if item_update.status == ItemStatus.published:
        if item.owner_id != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=403, detail="Only owner or admin can publish items")

    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(item, key, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check permissions
    if item.owner_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}


@router.post("/{item_id}/publish", response_model=ItemPublic)
async def publish_item(
    item_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check permissions
    if item.owner_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if item.status == ItemStatus.published:
        raise HTTPException(
            status_code=400, detail="Item is already published")

    item.status = ItemStatus.published
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
