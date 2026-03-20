"""Accounts API router (社媒账号管理)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import SocialAccount
from app.schemas import AccountPositioningUpdate, MessageResponse, SocialAccountOut

router = APIRouter(prefix="/accounts", tags=["账号管理 Accounts"])


@router.get("", response_model=list[SocialAccountOut])
async def list_accounts(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取当前用户绑定的所有社媒账号."""
    result = await db.execute(
        select(SocialAccount).where(SocialAccount.owner_id == current_user.id)
    )
    return [SocialAccountOut.model_validate(a) for a in result.scalars()]


@router.get("/{account_id}", response_model=SocialAccountOut)
async def get_account(
    account_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(SocialAccount).where(
            SocialAccount.id == account_id, SocialAccount.owner_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise NotFoundError("Account not found")
    return SocialAccountOut.model_validate(account)


@router.put("/{account_id}/positioning", response_model=SocialAccountOut)
async def update_positioning(
    account_id: str,
    data: AccountPositioningUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """更新账号定位信息（阶段、领域、标签）."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(SocialAccount).where(
            SocialAccount.id == account_id, SocialAccount.owner_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise NotFoundError("Account not found")
    current_pos = dict(account.positioning or {})
    update = data.model_dump(exclude_none=True)
    current_pos.update(update)
    account.positioning = current_pos
    await db.flush()
    return SocialAccountOut.model_validate(account)


@router.delete("/{account_id}", response_model=MessageResponse)
async def disconnect_account(
    account_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """解绑社媒账号."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(SocialAccount).where(
            SocialAccount.id == account_id, SocialAccount.owner_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise NotFoundError("Account not found")
    account.is_active = False
    await db.flush()
    return MessageResponse.ok("账号已解绑")
