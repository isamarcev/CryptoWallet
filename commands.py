import asyncio

import typer

from base_api.config.commands.admin import create_user_admin

app = typer.Typer()


@app.command()
def create_admin():
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(create_user_admin())
    asyncio.run(create_user_admin())
    print('admin was created')


@app.command()
def create_products():
    print('product was created')


if __name__ == "__main__":
    app()
