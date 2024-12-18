from datetime import datetime

from sqlalchemy import String, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    sku: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    offers: Mapped[list['Offer']] = relationship(back_populates='product')

class Offer(Base):
    __tablename__ = 'offers'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    availability: Mapped[str] = mapped_column(String, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    product: Mapped['Product'] = relationship(back_populates='offers')