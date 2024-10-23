from typing import Type

from fastapi import APIRouter
from fastapi_users import FastAPIUsers as APIUsers, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from ..db.models.users import User
from ..dependencies.auth import get_strategy, get_user_manager
from .transport import BaseTransport
from .strategy import BaseStrategy
from .api.auth import get_auth_router


def _st():
    return BaseStrategy()


transport = BaseTransport()

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=_st,
)


class FastAPIUsers(APIUsers[User, int]):

    def get_auth_router(
            self, backend: AuthenticationBackend, requires_verification: bool = False
    ) -> APIRouter:
        return get_auth_router(backend, self.get_user_manager,
                               self.authenticator, requires_verification)


fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
