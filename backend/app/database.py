from sqlalchemy import select

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import DATABASE_URL
from app.models import Post, PostRequest, Base


engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# декоратор создания сессии
def connection(method):
	async def wrapper(*args, **kwargs):
		async with async_session_maker() as session:
			try:
				return await method(*args, session=session, **kwargs)
			except Exception as e:
				await session.rollback()
				raise e
			finally:
				await session.close()
	return wrapper


@connection
async def get_all_posts_from_db(session: AsyncSession) -> list[Post]:
    result = await session.execute(select(Post))
    return result.scalars().all()


@connection
async def get_post_from_db(post_id: int, session: AsyncSession) -> Post | None:
    result = await session.execute(select(Post).where(Post.post_id == post_id))
    return result.scalar_one_or_none()


@connection
async def delete_post_from_db(post_id: int, session: AsyncSession):
    result = await session.execute(select(Post).where(Post.post_id == post_id))
    post = result.scalar_one_or_none()
    if post:
        await session.delete(post)
        await session.commit()
    return post


@connection
async def create_post_on_db(data: PostRequest, session: AsyncSession):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()


@connection
async def update_post_on_db(
    post_id: int, data: PostRequest, session: AsyncSession):
    result = await session.execute(select(Post).where(Post.post_id == post_id))
    post = result.scalar_one_or_none()
    if post:
        post.title = data.title
        post.content = data.content
        post.category = data.category
        post.tags = data.tags
        await session.commit()
    return post


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
