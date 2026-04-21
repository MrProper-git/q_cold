from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from fastapi import Depends

engine = create_async_engine('sqlite+aiosqlite:///leads.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class LeadsModel(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str]
    name: Mapped[str]
    contact: Mapped[str]
    text: Mapped[str | None] = mapped_column(nullable=True)
    notified: Mapped[bool] = mapped_column(default=False)
    processed: Mapped[bool] = mapped_column(default=False)

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)