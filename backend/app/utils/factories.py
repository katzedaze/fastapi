from sqlmodel import Session
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app.core.security import get_password_hash
from app.db.session import engine
from app.models.item import Item
from app.models.user import User
from app.models.enums import UserRole, ItemStatus, ItemCategory

fake = Faker()

# Create a session for factory_boy
session = Session(engine)


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    full_name = factory.Faker("name")
    hashed_password = factory.LazyFunction(
        lambda: get_password_hash("password123"))
    is_active = True
    role = factory.Faker("random_element", elements=[
                         UserRole.user, UserRole.guest])


class ItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text", max_nb_chars=500)
    price = factory.Faker("pyfloat", positive=True,
                          min_value=1, max_value=1000)
    quantity = factory.Faker("random_int", min=1, max=100)
    category = factory.Faker("random_element", elements=[
                             ItemCategory.electronics, ItemCategory.clothing, ItemCategory.books, ItemCategory.food, ItemCategory.other])
    status = factory.Faker("random_element", elements=[
                           ItemStatus.draft, ItemStatus.published, ItemStatus.archived])
    is_available = True
    owner_id = factory.SubFactory(UserFactory)
