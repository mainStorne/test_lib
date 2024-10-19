from typing import Optional
from fastapi_users import models, BaseUserManager
from fastapi_users.authentication.strategy import Strategy, StrategyDestroyNotSupportedError
from base64 import b64encode


class BaseStrategyDestroyNotSupportedError(StrategyDestroyNotSupportedError):
    def __init__(self) -> None:
        message = "A Base Authentication can't be invalidated"
        super().__init__(message)


class BaseStrategy(Strategy):

    async def read_token(
            self, token: Optional[str], user_manager: BaseUserManager[models.UP, models.ID]
    ) -> Optional[models.UP]:
        pass

    async def write_token(self, user: models.UP) -> str:
        base_string = f'{user.username}:{user.hashed_password}'
        return b64encode(base_string).decode()

    async def destroy_token(
            self, token: str, user: models.UP
    ) -> None:
        raise BaseStrategyDestroyNotSupportedError
