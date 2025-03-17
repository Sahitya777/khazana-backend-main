from pydantic import BaseModel
from datetime import date
from typing import List

# Existing User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True

# New Mutual Fund Schemas
class MutualFundBase(BaseModel):
    name: str
    isin: str

class MutualFundCreate(MutualFundBase):
    pass

class MutualFundResponse(MutualFundBase):
    id: int

    class Config:
        from_attributes = True

class InvestmentBase(BaseModel):
    mutual_fund_id: int
    investment_date: date
    amount_invested: float
    nav_at_investment: float
    returns_percentage: float

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentResponse(InvestmentBase):
    id: int

    class Config:
        from_attributes = True
