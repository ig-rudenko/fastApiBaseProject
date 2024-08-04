from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import func

from app.crud.manager import Manager
from app.orm.base_model import OrmBase


class User(OrmBase, Manager):
    """Модель пользователя"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(150))
    last_name: Mapped[Optional[str]] = mapped_column(String(150))
    email: Mapped[Optional[str]] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(128))

    date_join: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column()

    is_superuser: Mapped[bool] = mapped_column(server_default=false())
    is_staff: Mapped[bool] = mapped_column(server_default=false())

    is_active: Mapped[bool] = mapped_column(server_default=true())
    """Имеет ли пользователь возможность заходить на сайт."""

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username}>"


# Add other models here
