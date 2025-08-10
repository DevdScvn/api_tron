import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.wallet import WalletQueryDB

WALLET_ADDRESS = 'TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW'


@pytest.fixture(scope='function')
async def wallet_query(session: AsyncSession):
    '''Фикстура wallet_query'''
    wallet_query = WalletQueryDB(
        address=WALLET_ADDRESS,
        trx_balance=5148.03202,
        bandwidth=600,
        energy=0
    )
    session.add(wallet_query)
    await session.commit()
    await session.refresh(wallet_query)
    return wallet_query
