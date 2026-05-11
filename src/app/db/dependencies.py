from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncSession:
    session_factory = request.app.state.db_client

    async with session_factory() as session:
        yield session