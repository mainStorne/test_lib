from fastapi import APIRouter, Depends, Request, status, Response
from fastapi_sqlalchemy_toolkit import ModelManager
from fastapi_users.authentication import Authenticator
from pydantic import BaseModel
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession


def get_crud_router(manager: ModelManager, get_session, read_scheme: type[BaseModel],
                    create_scheme: type[BaseModel], update_scheme: type[BaseModel],
                    authenticator: Authenticator):
    crud = APIRouter()
    get_current_active_user = authenticator.current_user(
        active=True
    )

    auth_responses = {}

    get_current_superuser = authenticator.current_user(
        active=True, superuser=True
    )

    @crud.get('/', response_model=list[read_scheme])
    async def objects(request: Request, session: AsyncSession = Depends(get_session)):
        return await manager.list(session)

    @crud.post("/", response_model=read_scheme, responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorModel,
            "content": {
                "application/json": {}
            }
        }
    }, status_code=status.HTTP_201_CREATED)
    async def new(request: Request, objs: create_scheme, session: AsyncSession = Depends(get_session)):
        return await manager.create(session, objs)

    @crud.patch("/{id}", response_model=read_scheme, responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "content": {
                "application/json": {}
            }
        },
    })
    async def object(request: Request, id: int, scheme: update_scheme, session: AsyncSession = Depends(get_session)):
        model = await manager.get_or_404(session, id=id)
        return await manager.update(session, model, scheme)

    @crud.get("/{id}", response_model=read_scheme, responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "content": {
                "application/json": {}
            }
        }
    })
    async def object(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        return await manager.get_or_404(session, id=id)

    @crud.delete("/{id}",
                 dependencies=[Depends(get_current_superuser)],
                 response_class=Response,
                 responses={
                     status.HTTP_404_NOT_FOUND: {
                         "model": ErrorModel,
                         "content": {
                             "application/json": {}
                         }
                     },
                     status.HTTP_401_UNAUTHORIZED: {
                         "description": "Missing token or inactive user.",
                     },
                     status.HTTP_403_FORBIDDEN: {
                         "description": "Not a superuser.",
                     },
                 }, status_code=status.HTTP_204_NO_CONTENT)
    async def object(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        obj_in_db = await manager.get_or_404(session, id=id)
        await manager.delete(session, obj_in_db)
        return

    return crud
