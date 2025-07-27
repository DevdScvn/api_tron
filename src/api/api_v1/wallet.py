from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.swallet import SWalletRead, SWalletCreate, SWallet
from dao.walletdao import WalletDAO
from file_service.service import tron

router = APIRouter(tags=["Wallet"])


@router.get("", response_model=list[SWalletRead])
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        offset: int = 0,
        limit: int = 10,
):
    query = await WalletDAO.get_objects_or_404(
        session, offset, limit
    )
    return query


@router.post('/', response_model=SWallet)
async def get_info_about_address(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    query_create: SWalletCreate,
):
    wallet_info = await tron.get_wallet_info(query_create.address)
    await WalletDAO.add_wallet_request(session, wallet_info)
    return wallet_info
