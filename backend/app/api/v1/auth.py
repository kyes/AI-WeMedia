"""Auth API router."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.schemas import MessageResponse, PasswordChange, TokenRefresh, TokenResponse, UserLogin, UserOut, UserRegister, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证 Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """注册新用户."""
    svc = AuthService(db)
    user = await svc.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """账号密码登录，返回 JWT Token 对."""
    svc = AuthService(db)
    return await svc.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    """使用 refresh_token 换取新的 access_token."""
    svc = AuthService(db)
    return await svc.refresh(data.refresh_token)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: CurrentUser):
    """获取当前登录用户信息."""
    return current_user


@router.put("/me", response_model=UserOut)
async def update_me(data: UserUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """更新当前用户资料."""
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    await db.flush()
    return current_user


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    data: PasswordChange, current_user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    """修改密码."""
    from app.core.security import hash_password, verify_password
    from app.core.exceptions import BadRequestError
    if not verify_password(data.current_password, current_user.hashed_password):
        raise BadRequestError("当前密码错误")
    current_user.hashed_password = hash_password(data.new_password)
    await db.flush()
    return MessageResponse.ok("密码修改成功")
