import enum

from sqlalchemy import Column, Integer, ForeignKey, String, Text, ARRAY, Enum
from sqlalchemy.orm import relationship

from API.core.database.base import Base


class HandicraftCategory(enum.Enum):
    KNITTING = "knitting"                # В'язання
    CROCHET = "crochet"                  # В'язання гачком
    JEWELRY = "jewelry"                  # Прикраси
    SEWING = "sewing"                    # Шиття
    EMBROIDERY = "embroidery"            # Вишивка
    PAINTING = "painting"                # Розпис, малювання
    WOODWORK = "woodwork"                # Деревообробка
    LEATHER_CRAFT = "leather_craft"      # Вироби з шкіри
    CERAMICS = "ceramics"                # Кераміка, глина
    CANDLE_MAKING = "candle_making"      # Свічки
    SOAP_MAKING = "soap_making"          # Мило
    PAPER_CRAFT = "paper_craft"          # Паперові вироби (орігамі, скрапбукінг)
    GLASS_ART = "glass_art"              # Вітражі, фьюзинг, скло
    METAL_CRAFT = "metal_craft"          # Металопластика
    RESIN_ART = "resin_art"              # Епоксидна смола
    BASKETRY = "basketry"                # Плетіння кошиків
    DOLL_MAKING = "doll_making"          # Ляльки ручної роботи
    MACRAME = "macrame"                  # Макраме (вузлове плетіння)
    OTHER = "other"                      # Інше\
class PostStatus(enum.Enum):
    SOLD = "sold"
    IN_STOCK = "in_stock"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Автор поста
    title = Column(String(50), nullable=False)  # Заголовок поста
    content = Column(Text, nullable=False)  # Текст поста
    image_url = Column(String(100), nullable=True)  # Фото до поста (опціонально)
    categories = Column(ARRAY(Enum(HandicraftCategory, name="category")), nullable=True)
    credit_card_number = Column(String(16), nullable=True)
    status = Column(Enum(PostStatus, name="status"), nullable=True)

    user = relationship("User", backref="posts")
    reviews = relationship("Review", back_populates="post", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="post", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Хто залишив відгук
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)  # На який пост
    message = Column(Text, nullable=True)  # Текст відгуку
    rating = Column(Integer, nullable=False)  # Оцінка (1-5)

    user = relationship("User", back_populates="reviews")
    post = relationship("Post", back_populates="reviews")