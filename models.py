from uuid import uuid4
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class CategoryORM(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    guides: Mapped[list["GuideORM"]] = relationship('GuideORM',back_populates="category", cascade="all, delete-orphan")
class GuideORM(Base):
    __tablename__ = "guides"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category_id: Mapped[str] = mapped_column(String, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category: Mapped['CategoryORM'] = relationship('CategoryORM', back_populates="guides")