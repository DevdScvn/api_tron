from datetime import datetime

from pydantic import BaseModel


class SWallet(BaseModel):
    address: str
    trx_balance: float
    bandwidth: int
    energy: int


class SWalletRead(SWallet):
    id: int
    created_at: datetime


class SWalletCreate(BaseModel):
    address: str

