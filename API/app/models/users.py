from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from API.core.database.base import Base
from API.core.database.mixins.timestamp import TimestampMixin


class User(Base,TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True, nullable=False)  # ID від Google
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")



class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)

    user = relationship("User", back_populates="favorites")
    post = relationship("Post", back_populates="favorites")