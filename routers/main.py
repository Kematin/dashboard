from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import config
from service.session import SessionData, cookie, create_session, verifier

router = APIRouter(tags=["Main"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def dashboard_page(
    request: Request, session_data: SessionData | None = Depends(verifier)
):
    # if session_data is None:
    #     return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_system(
    request: Request,
    response: Response,
    username: str = Form("username"),
    password: str = Form("password"),
):
    if username == config.admin.username and password == config.admin.password:
        cookies = await create_session(request, response)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(**cookies)
        return response
    return templates.TemplateResponse("login.html", {"request": request})
