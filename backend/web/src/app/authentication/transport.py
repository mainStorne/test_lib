from fastapi_users.authentication.transport import Transport
from fastapi.security.http import HTTPBasic
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from fastapi_users.openapi import OpenAPIResponseType
from starlette.responses import Response


class BaseTransport(Transport):
    scheme = HTTPBasic

    def __init__(self):
        self.scheme = HTTPBasic(realm='realm')

    async def get_login_response(self, token: str) -> Response:
        return Response(headers={'Authorization': f'Basic {token}'})

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {}

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        return {}
