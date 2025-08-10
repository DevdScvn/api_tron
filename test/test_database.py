import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession




@pytest.mark.asyncio
async def test_get_latest_query(
    session: AsyncSession, wallet_query: WalletQueryDB
):
    '''Проверка добаления новой записи в БД'''
    stmt = select(WalletQueryDB)
    result: Result = await session.execute(stmt)
    wallet = result.scalars().first()
    assert wallet.address == wallet_query.address
    assert wallet.trx_balance == wallet_query.trx_balance
    assert wallet.bandwidth == wallet_query.bandwidth
    assert wallet.energy == wallet_query.energy
    assert wallet.id == wallet_query.id
    assert wallet.timestamp == wallet_query.timestamp
