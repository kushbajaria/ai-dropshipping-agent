from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    supplier: Mapped[str] = mapped_column(String(255))
    cost: Mapped[float] = mapped_column(Float)
    sale_price: Mapped[float] = mapped_column(Float)
    niche: Mapped[str] = mapped_column(String(100))
