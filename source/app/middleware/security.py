from json import loads

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session as SQLAlchemySession
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.types import ASGIApp
from app.data.database import engine
import geocoder

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
    
    Session = SQLAlchemySession(engine)

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
            # auth = request.headers.get('Authorization')
            client_host = request.client.host
            _path = request.scope['path']
            
            # disponibilizar o Swagger
            # if _path in ['/docs']:
            if _path in ['/docs', '/openapi.json']:
                response = await call_next(request)
                return response
                
            if client_host:
                geolocation = await self.get_geolocation(client_host=client_host)
                request.state.geolocation = geolocation
                
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


    async def get_current_tenant(self, authorization: str, path: str, session: SQLAlchemySession):
        """get_current_tenant Verifica se tem tenant e verifica se o path é permitido para esse Requisitante

        Args:
            authorization (str): Token recebido
            path (str): Path da requisição
            session (SQLAlchemySession): Conector com o Banco de Dados

        Raises:
            credentials_exception: Access forbidden for tenant
            HTTPException: Authorization missing for path

        Returns:
            _type_: Int
        """
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden: Access forbidden',
        )
        # TODO:Incluir em models futuramente.
        class LogItem:
            ...
        
        auth = f"{authorization[:10]}...{authorization[-10:]}"
        log_item = session.scalar(select(LogItem).where(LogItem.partial_token == str(auth)))

        if log_item is None or log_item.tenant is None:
            raise credentials_exception

        scopes = loads(log_item.roles_scope) if log_item.roles_scope else []
        
        if path not in scopes and "all" not in scopes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        session.refresh(log_item)

        return log_item.tenant


def get_current_tenant(request: Request) -> int:
    """get_current_tenant Retorna o tenant pego na verificação, para que seja utilizado para validar se o requisitante pode fazer a solição corrente.

    Args:
        request (Request): Requisição após validado

    Raises:
        HTTPException: Tenant not found

    Returns:
        int: Int
    """
    tenant = getattr(request.state, "current_tenant", None)
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Tenant not found")
    return tenant


def get_current_domain(request: Request) -> str:
    """get_current_domain Retorna o ambiente passado pelo Outsystem para direcionamento correto dos ambientes.

    Args:
        request (Request): Requisição após validado

    Returns:
        str: str
    """
    return getattr(request.state, "client_domain", 'dev')
