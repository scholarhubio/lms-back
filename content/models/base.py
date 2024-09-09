from sqlalchemy import String, DateTime, Integer, func, Boolean
from sqlalchemy.orm import declared_attr, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.future import select
from sqlalchemy.orm import Session
import uuid
from slugify import slugify
from datetime import datetime
from typing import Any, Dict, Optional


class Base(AsyncAttrs, DeclarativeBase):
    """Base class with AsyncAttrs for async SQLAlchemy models."""

    __abstract__ = True  # Mark as abstract

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimeStampMixin:
    """Mixin to add created and modified timestamps."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class BaseModel(Base, TimeStampMixin):
    """Base model that includes UUID and timestamp mixins."""
    __abstract__ = True


class ContentBaseModel(BaseModel):
    """Content model with title and slug fields."""

    __abstract__ = True

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True)

    async def save(self, session: Session) -> None:
        """Save instance asynchronously and generate slug if not set."""
        if not self.slug:
            self.slug = slugify(self.title)
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return self.title


class OrderedModel(Base):
    """Model for objects with a customizable ordering scope."""

    __abstract__ = True

    order: Mapped[int] = mapped_column(Integer, default=0)

    async def save(self, session: Session) -> None:
        """Save the instance and determine its order based on the scope."""
        if self.order == 0:  # Assuming the order is set only on creation
            max_order_query = select(func.max(self.__class__.order)).filter_by(**self.get_ordering_scope())
            max_order = await session.execute(max_order_query)
            max_order_value = max_order.scalar_one_or_none()
            self.order = (max_order_value or 0) + 1
        
        session.add(self)
        await session.commit()

    def get_ordering_scope(self) -> Dict[str, Any]:
        """Defines the ordering scope, should be overridden in subclasses."""
        return {}
