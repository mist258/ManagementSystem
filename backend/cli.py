import asyncio
import click
from sqlalchemy import select
from api.auth.utils import hash_password
from core.models.db_helper import db_helper
from api.users.models import User, UserProfile

@click.group()
def cli():
    pass

@cli.command()
@click.option('--first_name', prompt='First name')
@click.option('--last_name', prompt='Last name')
@click.option('--email', prompt='Email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def create_superuser(first_name, last_name, email: str, password: str):
    """
        Create a superuser account
        """
    asyncio.run(_create_superuser(first_name, last_name, email, password))

async def _create_superuser(first_name: str, last_name: str, email: str, password: str):
    async with db_helper.session_factory() as db:
        result = await db.execute(
            select(User).where(User.is_superuser == True)
        )
        if result.scalar_one_or_none():
            click.secho('Admin already exists!', fg='red')
            return
        try:
            user = User(
                email=email,
                hashed_password=hash_password(password),
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            db.add(user)
            await db.flush()

            profile = UserProfile(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name
            )
            db.add(profile)
            await db.commit()

            click.secho(f"Admin {email} created!", fg='green')
        except Exception as e:
            await db.rollback()
            click.secho(f"Error: {e}", fg='red')

if __name__ == '__main__':
    cli()







