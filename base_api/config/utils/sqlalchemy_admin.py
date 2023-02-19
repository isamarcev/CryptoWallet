from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request
from base_api.apps.users.models import user as user_table
from base_api.apps.chat.models import Message
from base_api.apps.ethereum.models import Wallet, Transaction
from base_api.apps.ibay.models import Product, Order
from base_api.apps.users.models import User, Permission
from base_api.base_api_consumer import async_session


class UserAdmin(ModelView, model=User):
    can_delete = False
    column_list = [User.username, User.email]


class PermissionAdmin(ModelView, model=Permission):
    can_delete = False
    column_list = [Permission.user_id]


class ProductAdmin(ModelView, model=Product):
    can_delete = False
    column_list = [Product.title, Product.price]


class OrderAdmin(ModelView, model=Order):
    can_delete = False
    column_list = [Order.id, Order.product, Order.datetime]


class WalletAdmin(ModelView, model=Wallet):
    can_delete = False
    column_list = [Wallet.public_key]
    form_excluded_columns = [Wallet.currency_type, Wallet.currency_name]


class TransactionAdmin(ModelView, model=Transaction):
    can_delete = False
    column_list = [Transaction.number, Transaction.status]
    form_excluded_columns = [Transaction.status]


class MessageAdmin(ModelView, model=Message):
    can_delete = False
    column_list = [Message.id]


class MyBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with async_session() as session:
            try:
                result = await session.execute(
                    select(User).where(user_table.c.email == username))
                user = result.scalars().first()
            finally:
                await session.close()


        print(user.email)


        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token
        return True


authentication_backend = MyBackend(secret_key="hudshuifw32434jfdbeqiu23djth344hef34uith")
