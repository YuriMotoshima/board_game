from json import loads

import geocoder
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session as SQLAlchemySession
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.types import ASGIApp

from app.data.database import async_session
from app.models.CacheData import CacheData


class HeaderValidationMiddleware(BaseHTTPMiddleware):
    """HeaderValidationMiddleware Middleware.

    Args:
        BaseHTTPMiddleware (_type_): Middleware

    Raises:
        HTTPException: Authorization missing for path
        credentials_exception: Access forbidden for tenant
        HTTPException: Error server

    Returns:
        _type_: None
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """dispatch acessa a requisição para identificar o path e o token e de acordo com as validações muda o state da request.
    

        Args:
            request (Request): Requisição recebida
            call_next (RequestResponseEndpoint): Envia pra o a rota se passado pelas validações

        Raises:
            HTTPException: Forbidden quando identificado pontos na validação do tenant e do escopo.

        Returns:
            _type_: Response
        """
        try:
            client_host = request.client.host
            headers_dict = {key: value for key, value in request.headers.items()}
            scope_cleaned = {
                key: str(value) if isinstance(value, (dict, list, str, int, float)) else repr(value)
                for key, value in request.scope.items()
            }
            _path = request.scope['path']
            
            # disponibilizar o Swagger
            # 0 =Route(path='/openapi.json', name='openapi', methods=['GET', 'HEAD'])
            # 1 =Route(path='/docs', name='swagger_ui_html', methods=['GET', 'HEAD'])
            # 2 =Route(path='/docs/oauth2-redirect', name='swagger_ui_redirect', methods=['GET', 'HEAD'])
            # 3 =Route(path='/redoc', name='redoc_html', methods=['GET', 'HEAD'])
            # 4 =APIRoute(path='/', name='read_root', methods=['GET'])
            
            # if _path in ['/docs']:
            if _path in ['/docs', '/openapi.json']:
                response = await call_next(request)
                return response
                
            if client_host:
                request.state.user_language = request.headers.get("Accept-Language")
                request.state.user_agent = request.headers.get("User-Agent")
                request.state.path = _path
                request.state.client_host = client_host
                request.state.headers = headers_dict
                request.state.scopes = scope_cleaned
                request.state.geolocation = await self.get_geolocation(client_host=client_host)
                
                async with async_session() as session:
                    cache_data = await self.updated_cachedata(state=request.state._state, session=session)
                    request.state.cache_data = cache_data
                
            response = await call_next(request)
            return response

        except HTTPException as err:
            return JSONResponse(status_code=err.status_code, content={"detail": err.detail})
        except Exception as err:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "server"})


    async def get_geolocation(self, client_host: Request):
        geo = geocoder.ip(client_host)

        if geo.ok:
            return {
                "city": geo.city or "-",
                "state": geo.state or "-",
                "country": geo.country or "-",
                "latitude": geo.lat or "-",
                "longitude": geo.lng or "-"
            }
        else:
            return {"error": "Geolocation not found"}
        

    async def updated_cachedata(self, state:dict, session:AsyncSession) -> CacheData:
        cache = CacheData(**state)
        session.add(cache)
        await session.commit()
        await session.refresh(cache)
        return cache