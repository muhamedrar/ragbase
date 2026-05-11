from fastapi import Request


async def get_db_session(request: Request) :
    session_factory = request.app.state.db_client

    async with session_factory() as session:
        yield session