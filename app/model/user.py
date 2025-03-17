from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base
import json

class User(Base):
    __tablename__ = "credentials"

    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String)

# Mutual Fund Models
class MutualFund(Base):
    __tablename__ = "mutual_funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    isin = Column(String, unique=True, nullable=False)
    nav = Column(Integer, unique=False, nullable=False)

    investments = relationship("Investment", back_populates="mutual_fund")
    allocations = relationship("Allocation", back_populates="mutual_fund")
    overlaps1 = relationship("Overlap", foreign_keys="[Overlap.fund_1_id]", back_populates="fund_1")
    overlaps2 = relationship("Overlap", foreign_keys="[Overlap.fund_2_id]", back_populates="fund_2")


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    mutual_fund_id = Column(Integer, ForeignKey("mutual_funds.id", ondelete="CASCADE"), nullable=False)
    investment_date = Column(Date, nullable=False)
    amount_invested = Column(Numeric(15,2), nullable=False)
    nav_at_investment = Column(Numeric(10,2), nullable=False)
    returns_percentage = Column(Numeric(5,2), nullable=False)

    mutual_fund = relationship("MutualFund", back_populates="investments")


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    mutual_fund_id = Column(Integer, ForeignKey("mutual_funds.id", ondelete="CASCADE"), nullable=False)
    mutualfund_name = Column(String, nullable=False)
    sector_allocation = Column(JSON, nullable=False)  # Example: {"IT": 38, "Financials": 37, "Energy": 25}
    stock_allocation = Column(JSON, nullable=False)   # Example: {"Reliance": 25, "HDFC Bank": 22, "TCS": 20}
    market_cap_allocation = Column(JSON, nullable=False)  # Example: {"Large Cap": 98, "Mid Cap": 2, "Small Cap": 0}

    mutual_fund = relationship("MutualFund", back_populates="allocations")


class Overlap(Base):
    __tablename__ = "overlaps"

    id = Column(Integer, primary_key=True, index=True)
    fund_1_id = Column(Integer, ForeignKey("mutual_funds.id", ondelete="CASCADE"), nullable=False)
    fund_2_id = Column(Integer, ForeignKey("mutual_funds.id", ondelete="CASCADE"), nullable=False)
    overlap_percentage = Column(Numeric(5,2), nullable=False)

    fund_1 = relationship("MutualFund", foreign_keys=[fund_1_id], back_populates="overlaps1")
    fund_2 = relationship("MutualFund", foreign_keys=[fund_2_id], back_populates="overlaps2")
