from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Wallet
from core.schemas.swallet import SWalletRead
from dao.basedao import BaseDAO


class WalletDAO(BaseDAO):
    model = Wallet

    @staticmethod
    async def add_wallet_request(
            session: AsyncSession,
            wallet_query: dict
    ) -> SWalletRead:

        '''Добавление новой записи в БД'''
        wallet = Wallet(**wallet_query)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet
