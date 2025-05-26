from app.utils.factories import UserFactory, ItemFactory
from app.models.item import Item
from app.models.user import User
from app.models.enums import UserRole
from app.db.session import engine
from app.core.security import get_password_hash
from sqlmodel import Session, SQLModel, select
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def seed_database():
    """Seed the database with initial data."""
    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Check if data already exists
        statement = select(User)
        existing_users = len(session.exec(statement).all())
        if existing_users > 0:
            print("Database already seeded. Skipping...")
            return

        print("Seeding database...")

        # Create a superuser
        superuser = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            role=UserRole.admin,
        )
        session.add(superuser)
        session.commit()
        session.refresh(superuser)
        print(f"Created superuser: {superuser.email}")

        # Create regular users
        users = []
        for i in range(5):
            user = UserFactory()
            users.append(user)
            print(f"Created user: {user.email}")

        # Create items for each user
        for user in users:
            for j in range(3):
                item = ItemFactory(owner_id=user.id)
                print(f"Created item: {item.title} for user {user.email}")

        # Create items for superuser
        for k in range(2):
            item = ItemFactory(owner_id=superuser.id)
            print(f"Created item: {item.title} for superuser")

        print("Database seeding completed!")


if __name__ == "__main__":
    seed_database()
