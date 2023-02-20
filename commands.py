import asyncio

import typer

from base_api.config.app import app
from base_api.config.commands.init import ProjectInitialization

app_typer = typer.Typer()


@app_typer.command()
def create_admin():
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(create_user_admin())
    asyncio.run(ProjectInitialization.start(app))
    print('admin was created')


@app_typer.command()
def create_products():
    print('product was created')


if __name__ == "__main__":
    app_typer()
