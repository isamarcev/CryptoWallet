import asyncio
import concurrent
import functools
import re
from typing import Dict

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base_api.apps.users.database import UserDatabase
from base_api.apps.users.schemas import UserRegister


async def validate_email_(email: str) -> Dict:
    result = {}
    try:
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            validation = await loop.run_in_executor(
                pool, functools.partial(validate_email, email=email, check_deliverability=True))
        email = validation.email
        result["valid"] = email
    except EmailNotValidError as e:
        result["invalid"] = str(e)
    return result


async def validate_password(password: str) -> bool:
    match = re.match("(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}", password)
    return True if match else False


async def validate_username(username: str) -> bool:
    if re.match(r"^[\w\d +]{5,40}$", username) and len([letter for letter in username if letter.isalpha()]) >= 4:
        return True
    return False


async def validate_register(user: UserRegister, session: AsyncSession, user_db: UserDatabase ):
    errors = {"errors": {}}
    validated_email = await validate_email_(user.email)
    if validated_email.get("valid"):
        user.email = validated_email["valid"]
        if await user_db.get_user_by_email(user.email, session):
            errors["errors"]["email"] = "Email is already registered"
    else:
        errors["errors"]["email"] = validated_email["invalid"]
    validated_password = await validate_password(user.password)
    if not validated_password:
        errors["errors"]["password"] = ("Password must contain at least: one digit, "
                                        "one uppercase letter, one lowercase letter,"
                                        " one special character[$@#], 8 to 20 characters")
    if user.password != user.password2:
        errors["errors"]["mismatch_password"] = "Password missmatch"
    if not await validate_username(user.username):
        errors["errors"]["username"] = "Invalid username"
    if await user_db.get_user_by_username(user.username, session):
        errors["errors"]["username"] = "Username is already registered"
    if errors.get("errors"):
        return errors
    return {"success_validation": True}

