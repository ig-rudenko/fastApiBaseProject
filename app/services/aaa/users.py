import re
from typing import Optional

from fastapi import Depends, Header, HTTPException, Form
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.orm.session_manager import get_session
from app.schemas.users import UserCreateSchema, UserCredentialsSchema
from app.services.encrypt import encrypt_password, validate_password
from .exc import CredentialsException, UserNotActiveException
from .jwt import oauth2_scheme, _get_token_payload, USER_IDENTIFIER


def get_user_credentials(
    user_data: UserCredentialsSchema | None = None,
    username: str = Form(""),
    password: str = Form(""),
) -> UserCredentialsSchema:
    if not (user_data or username) or not (user_data or password):
        raise HTTPException(status_code=422, detail="Username and password is required")
    return UserCredentialsSchema(
        username=username or user_data.username, password=password or user_data.password
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session, use_cache=True),
) -> User:
    """
    Получение текущего пользователя по токену аутентификации.

    :param token: Токен пользователя.
    :param session: :class:`AsyncSession` объект сессии.
    :return: Объект пользователя :class:`User`.
    :raises CredentialsException: Если пользователь не найден.
    """
    payload = _get_token_payload(token, "access")
    try:
        user = await User.get(session, id=payload[USER_IDENTIFIER])
    except NoResultFound:
        raise CredentialsException
    if not user.is_active:
        raise UserNotActiveException
    return user


async def get_user_or_none(
    authorization: Optional[str] = Header(None), session: AsyncSession = Depends(get_session, use_cache=True)
) -> User | None:
    """
    Получение текущего пользователя по токену аутентификации либо None.

    :param authorization: Значение заголовка HTTP (Authorization).
    :param session: :class:`AsyncSession` объект сессии.
    :return: Объект пользователя :class:`User` или :class:`None`.
    :raises CredentialsException: Если пользователь не найден.
    """
    if authorization:
        if token_match := re.match(r"Bearer (\S+)", authorization):
            try:
                return await get_current_user(token_match.group(1), session)
            except HTTPException:
                return None
    return None


async def create_user(session: AsyncSession, user: UserCreateSchema) -> User:
    user_data = user.model_dump()
    user_data["password"] = encrypt_password(user_data["password"])
    obj = User(username=user_data["username"], email=user_data["email"], password=user_data["password"])
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def get_user_by_credentials(session: AsyncSession, username: str, password: str) -> User:
    try:
        user_model = await User.get(session, username=username)
    except NoResultFound:
        raise CredentialsException

    if not validate_password(password, user_model.password):
        raise CredentialsException
    return user_model
