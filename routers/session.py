from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response

from service.session import SessionData, backend, cookie, create_session, verifier

router = APIRouter(prefix="/session", tags=["Session"])


@router.get("/create")
async def create_session_route(request: Request, response: Response):
    await create_session(request, response)
    return "Ok"


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
