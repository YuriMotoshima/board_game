from jwt import decode

from app.security.security import create_access_token

def test_created_token_updated_expire(settings):
    data={"sub":"test@test.com"}
    result = create_access_token(data=data)
    
    decoded = decode(result, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]