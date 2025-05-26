from typing import Annotated, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col

from app.api.deps import get_current_active_user, get_current_admin_user
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.user import User, UserCreate, UserPublic, UserUpdate, UserPublicWithItems
from app.models.enums import UserRole

router = APIRouter()


@router.post("/", response_model=UserPublic)
async def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    statement = select(User).where(User.email == user.email)
    db_user = db.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.model_dump(exclude={"password"})
    user_dict["hashed_password"] = get_password_hash(user.password)

    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserPublicWithItems)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    # Refresh to get relationships
    db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserPublic])
async def read_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
):
    statement = select(User)

    if role:
        statement = statement.where(User.role == role)
    if is_active is not None:
        statement = statement.where(User.is_active == is_active)

    statement = statement.offset(skip).limit(limit)
    users = db.exec(statement).all()
    return users


@router.get("/{user_id}", response_model=UserPublicWithItems)
async def read_user(
    user_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check permissions
    if current_user.id != user_id and current_user.role != UserRole.admin:
        # Return basic info only
        return UserPublic.model_validate(user)

    return user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check permissions
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Only admin can change roles
    if user_update.role and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403, detail="Only admin can change user roles")

    user_data = user_update.model_dump(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(
            user_data.pop("password"))

    for key, value in user_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
