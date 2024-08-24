import re
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel

from config import config


class CustomSessionCookie(SessionCookie):
    def attach_to_response(self, response: Response, session_id: UUID) -> dict:
        value = str(self.signer.dumps(session_id.hex))
        key = self.model.name
        cookies = {
            "key": key,
            "value": value,
        } | dict(self.cookie_params)
        response.set_cookie(**cookies)
        return cookies


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()

cookie = CustomSessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=False,
    secret_key=config.api.session_secret,
    cookie_params=cookie_params,
)

backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


async def create_session(request: Request, response: Response) -> dict:
    x = "x-forwarded-for".encode("utf-8")
    for header in request.headers.raw:
        if header[0] == x:
            print("Find out the forwarded-for ip address")
            origin_ip, forward_ip = re.split(", ", header[1].decode("utf-8"))
            print(f"origin_ip:\t{origin_ip}")
            print(f"forward_ip:\t{forward_ip}")
    name = config.admin.username
    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookies = cookie.attach_to_response(response, session)
    return cookies


async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
