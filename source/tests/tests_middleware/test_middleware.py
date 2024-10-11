import pytest
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import RequestResponseEndpoint

from app.middleware.middle import HeaderValidationMiddleware
from app.data.models import CacheData

@pytest.mark.asyncio
async def test_dispatch_with_valid_client(monkeypatch, mocker):
    # Mock request and call_next
    request = mocker.MagicMock(Request)
    request.scope = {"path": "/test"}
    request.headers = {
        "Accept-Language": "en-US",
        "User-Agent": "test-agent",
    }
    request.client.host = "127.0.0.1"
    
    response = mocker.MagicMock()

    async def mock_call_next(req):
        return response

    # Mock the get_geolocation method
    async def mock_get_geolocation(client_host):
        return {
            "city": "Test City",
            "state": "Test State",
            "country": "Test Country",
            "latitude": "123.456",
            "longitude": "789.123",
        }

    # Mock database session
    async def mock_updated_cachedata(state, session):
        return None

    monkeypatch.setattr(HeaderValidationMiddleware, "get_geolocation", mock_get_geolocation)
    monkeypatch.setattr(HeaderValidationMiddleware, "updated_cachedata", mock_updated_cachedata)

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert result == response
    assert request.state.geolocation["city"] == "Test City"
    assert request.state.user_language == "en-US"
    assert request.state.user_agent == "test-agent"


@pytest.mark.asyncio
async def test_dispatch_with_swagger_paths(mocker):
    request = mocker.MagicMock(Request)
    request.scope = {"path": "/docs"}
    response = mocker.MagicMock()

    async def mock_call_next(req):
        return response

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert result == response


@pytest.mark.asyncio
async def test_dispatch_with_500_error(monkeypatch, mocker):
    request = mocker.MagicMock(Request)
    request.scope = {"path": "/test"}
    request.client.host = "127.0.0.1"

    async def mock_call_next(req):
        raise Exception("Test Exception")

    async def mock_get_geolocation(client_host):
        return {"city": "-", "state": "-", "country": "-"}

    monkeypatch.setattr(HeaderValidationMiddleware, "get_geolocation", mock_get_geolocation)

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    result = await middleware.dispatch(request, mock_call_next)

    assert isinstance(result, JSONResponse)
    assert result.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert result.body == b'{"detail":"server"}'


@pytest.mark.asyncio
async def test_get_geolocation_success(mocker, monkeypatch):
    from geocoder import ip

    mock_geo = mocker.MagicMock()
    mock_geo.ok = True
    mock_geo.city = "Test City"
    mock_geo.state = "Test State"
    mock_geo.country = "Test Country"
    mock_geo.lat = "123.456"
    mock_geo.lng = "789.123"

    monkeypatch.setattr(ip, "return_value", mock_geo)

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    result = await middleware.get_geolocation(client_host="127.0.0.1")

    assert result["city"] == "Test City"
    assert result["state"] == "Test State"
    assert result["country"] == "Test Country"


@pytest.mark.asyncio
async def test_get_geolocation_failure(mocker, monkeypatch):
    from geocoder import ip

    mock_geo = mocker.MagicMock()
    mock_geo.ok = False

    monkeypatch.setattr(ip, "return_value", mock_geo)

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    result = await middleware.get_geolocation(client_host="127.0.0.1")

    assert result == {"error": "Geolocation not found"}


@pytest.mark.asyncio
async def test_updated_cachedata(mocker):
    mock_session = mocker.MagicMock(AsyncSession)
    mock_state = {
        "client_host": "127.0.0.1",
        "user_language": "en-US",
        "user_agent": "test-agent",
    }

    middleware = HeaderValidationMiddleware(app=mocker.MagicMock())
    await middleware.updated_cachedata(state=mock_state, session=mock_session)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
