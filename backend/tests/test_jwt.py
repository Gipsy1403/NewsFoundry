from src.auth.jwt import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt


def test_create_access_token_contains_payload():
    token = create_access_token({"user_id": 123})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["user_id"] == 123
