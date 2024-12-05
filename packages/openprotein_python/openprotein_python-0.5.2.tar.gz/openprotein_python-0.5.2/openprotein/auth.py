from openprotein.base import APISession
from openprotein.errors import AuthError, HTTPError

PATH_PREFIX = "v1/login"


def get_auth_token(session: APISession, username: str, password: str) -> str:
    endpoint = PATH_PREFIX + "/access-token"
    body = {"username": username, "password": password}
    try:
        response = session.post(endpoint, data=body, timeout=3)
    except HTTPError as e:
        # if an error occured during auth, we raise an AuthError with reference to the HTTPError
        raise AuthError(
            f"Authentication failed. Please check your credentials and connection."
        ) from e
    result = response.json()
    token = result.get("access_token")
    if token is None:
        raise AuthError("Unable to authenticate with given credentials.")
    return token
