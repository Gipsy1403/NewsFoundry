import pytest
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException

from src.auth.dependencies import get_current_user_id
from src.auth.jwt import create_access_token


def test_get_current_user_id_valid():
    token = create_access_token({"user_id": 7})
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    user_id = get_current_user_id(creds)
    assert user_id == 7


def test_get_current_user_id_invalid():
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="badtoken")
    with pytest.raises(HTTPException):
        get_current_user_id(creds)
