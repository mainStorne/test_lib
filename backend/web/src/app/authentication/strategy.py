from typing import Optional
from fastapi_users.authentication.strategy import Strategy, StrategyDestroyNotSupportedError
from pydantic import BaseModel, ValidationError
from base64 import b64encode
from ..conf import DJANGO_URL
from httpx import AsyncClient
from ..types.users import UserType
from ..managers.user import UserManager


class BaseStrategyDestroyNotSupportedError(StrategyDestroyNotSupportedError):
    def __init__(self) -> None:
        message = "A Base Authentication can't be invalidated"
        super().__init__(message)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None


class BaseStrategy(Strategy):

    async def read_token( # type: ignore
            self, token: Optional[str], user_manager: UserManager
    ) -> Optional[UserType]:
        async with AsyncClient() as client:
            content = (await client.get(f'{DJANGO_URL}/token', headers={'Authentication': token})).content
        try:
            return UserResponse.model_validate_json(content)
        except ValidationError:
            return None

    async def write_token(self, user: UserType) -> str:  # type: ignore
        base_string = f'{user.username}:{user.hashed_password}'
        return b64encode(base_string).decode()

    async def destroy_token(  # type: ignore
            self, token: str, user: UserType
    ) -> None:
        raise BaseStrategyDestroyNotSupportedError
