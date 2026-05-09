from fastapi import APIRouter, Depends, Response, Request, status, HTTPException
from src.interface_adapters.presenters.dependencies import get_login_use_case, get_refresh_token_use_case, get_logout_use_case
from src.interface_adapters.presenters.guards import get_current_user
from src.interface_adapters.presenters.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse,
             status_code=status.HTTP_200_OK)
async def login(req: LoginRequest, response: Response,
                uc=Depends(get_login_use_case)):
    try:
        res = await uc.execute(email=req.email, password=req.password)
        response.set_cookie(
            "refresh_token",
            res["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=1440 * 60)
        return {"access_token": res["access_token"], "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: Request, uc=Depends(get_refresh_token_use_case)):
    token = req.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        return await uc.execute(refresh_token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout", status_code=204)
async def logout(req: Request, response: Response, uc=Depends(
        get_logout_use_case), _=Depends(get_current_user)):
    token = req.cookies.get("refresh_token")
    if token:
        await uc.execute(refresh_token=token)
        response.delete_cookie("refresh_token", httponly=True)
