import asyncio

import click
from api.articles.models import Article
from api.auth.utils import hash_password
from api.users.models import User, UserProfile
from core.models import db_helper


async def _seed():
    """
        Seed data base by initial data
    """

    async with db_helper.session_factory() as db:
        try:
            editor = User(
                email="editor@test.com",
                hashed_password=hash_password("Editor213!"),
                is_active=True,
                is_staff=True,
                is_superuser=False
            )
            user1 = User(
                email="user1@test.com",
                hashed_password=hash_password("User123!"),
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            user2 = User(
                email="user2@test.com",
                hashed_password=hash_password("User321!"),
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            db.add_all([editor, user1, user2])
            await db.flush()

            editor_profile = UserProfile(user_id=editor.id, first_name="John", last_name="Smith")
            user1_profile = UserProfile(user_id=user1.id, first_name="Nick", last_name="Han")
            user2_profile = UserProfile(user_id=user2.id, first_name="Jane", last_name="Bush")
            db.add_all([editor_profile, user1_profile, user2_profile])
            await db.flush()

            articles = [
                Article(title="First article", content="Some text", author_id=user1_profile.id),
                Article(title="Second article", content="Some text", author_id=user1_profile.id),
                Article(title="Editor article", content="Some text", author_id=editor_profile.id),
                Article(title="Jane article", content="Some text", author_id=user2_profile.id),
            ]
            db.add_all(articles)
            await db.commit()
            click.secho("Database seeded successfully!", fg="green")
        except Exception as e:
            await db.rollback()
            click.secho(f"Error: {e}", fg="red")

@click.command()
def seed():
    asyncio.run(_seed())

if __name__ == "__main__":
    seed()