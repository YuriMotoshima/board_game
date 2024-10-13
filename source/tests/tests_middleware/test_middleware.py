from unittest.mock import MagicMock

import pytest
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import RequestResponseEndpoint

from app.data.models import CacheData
from app.middleware.middle import HeaderValidationMiddleware


@pytest.mark.asyncio
async def test_dispatch_with_valid_client(monkeypatch):
    # Mock request and call_next
    request = MagicMock(Request)
    request.scope = {"path": "/test"}
    request.headers = {
        "Accept-Language": "en-US",
        "User-Agent": "test-agent",
    }
    request.client.host = "127.0.0.1"

    response = MagicMock()

    async def mock_call_next(req):
        return response

    # Mock the get_geolocation method
    async def mock_get_geolocation(*args, **kwargs):
        return {
            "city": "Test City",
            "state": "Test State",
            "country": "Test Country",
            "latitude": "123.456",
            "longitude": "789.123",
        }

    # Mock database session
    async def mock_updated_cachedata(*args, **kwargs):
        return None

    monkeypatch.setattr(HeaderValidationMiddleware,
                        "get_geolocation", mock_get_geolocation)
    monkeypatch.setattr(HeaderValidationMiddleware,
                        "updated_cachedata", mock_updated_cachedata)

    middleware = HeaderValidationMiddleware(app=MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert result == response
    assert request.state.geolocation["city"] == "Test City"
    assert request.state.user_language == "en-US"
    assert request.state.user_agent == "test-agent"


@pytest.mark.asyncio
async def test_dispatch_with_swagger_paths():
    request = MagicMock(Request)
    request.scope = {"path": "/docs"}
    response = MagicMock()

    async def mock_call_next(*args, **kwargs):
        return response

    middleware = HeaderValidationMiddleware(app=MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert result == response


@pytest.mark.asyncio
async def test_dispatch_with_500_error(monkeypatch):
    request = MagicMock(Request)
    request.scope = {"path": "/test"}
    request.client.host = "127.0.0.1"

    async def mock_call_next(*args, **kwargs):
        raise Exception("Test Exception")

    async def mock_get_geolocation(*args, **kwargs):
        return {"city": "-", "state": "-", "country": "-"}

    monkeypatch.setattr(HeaderValidationMiddleware,
                        "get_geolocation", mock_get_geolocation)

    middleware = HeaderValidationMiddleware(app=MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert isinstance(result, JSONResponse)
    assert result.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert result.body == b'{"detail":"server"}'


@pytest.mark.asyncio
async def test_get_geolocation_success(monkeypatch):
    import geocoder
    request = MagicMock(Request)
    request.scope = {"path": "/docs"}

    mock_geo = MagicMock()
    mock_geo.ok = True
    mock_geo.city = "Test City"
    mock_geo.state = "Test State"
    mock_geo.country = "Test Country"
    mock_geo.lat = "123.456"
    mock_geo.lng = "789.123"

    # Função que retorna o mock_geo quando chamada
    def mock_geocoder_ip_ok(client_host):
        return mock_geo

    monkeypatch.setattr(geocoder, "ip", mock_geocoder_ip_ok)

    middleware = HeaderValidationMiddleware(app=MagicMock())
    result = await middleware.get_geolocation(client_host="127.0.0.1")

    assert result == {
        "city": "Test City",
        "state": "Test State",
        "country": "Test Country",
        "latitude": "123.456",
        "longitude": "789.123",
    }


@pytest.mark.asyncio
async def test_get_geolocation_failure(monkeypatch):
    import geocoder

    mock_geo = MagicMock()
    mock_geo.ok = False

    # Função que retorna o mock_geo quando chamada
    def mock_geocoder_ip_nok(client_host):
        return mock_geo

    monkeypatch.setattr(geocoder, "ip", mock_geocoder_ip_nok)

    middleware = HeaderValidationMiddleware(app=MagicMock())
    result = await middleware.get_geolocation(client_host="127.0.0.1")

    assert result == {"error": "Geolocation not found"}


@pytest.mark.asyncio
async def test_updated_cachedata():
    mock_session = MagicMock(AsyncSession)
    mock_state = {
        "user_language": None, 
        "user_agent": "Thunder Client (https://www.thunderclient.com)", 
        "path": "/users/", 
        "client_host": "127.0.0.1", 
        "headers": {
            "accept-encoding": "gzip, deflate, br", 
            "accept": "*/*", 
            "user-agent": "Thunder Client (https://www.thunderclient.com)", 
            "host": "127.0.0.1:8000", "connection": "close"
            }, "scopes": {
                "type": "http", 
                "asgi": '{"version": "3.0", "spec_version": "2.4"}', 
                "http_version": "1.1", 
                "server": '("127.0.0.1", 8000)', 
                "client": '("127.0.0.1", 63885)', 
                "scheme": "http", 
                "method": "GET", 
                "root_path": "", 
                "path": "/users/", 
                "raw_path": 'b"/users/"', 
                "query_string": 'b"test = aaa"', 
                "headers": '[]', 
                "state": "{}", 
                "app": "<fastapi.applications.FastAPI object at 0x000002433F2B1AC0>"
                }, 
            "geolocation": {"city": "-", "state": "-", "country": "-", "latitude": "-", "longitude": "-"}
            }

    middleware = HeaderValidationMiddleware(app=MagicMock())
    await middleware.updated_cachedata(state=mock_state, session=mock_session)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
