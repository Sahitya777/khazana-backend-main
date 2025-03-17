from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.database import get_db
from app.model.user import User, MutualFund, Investment, Allocation
from app.schema.schema import UserCreate, MutualFundResponse, InvestmentResponse
from app.utils.util import hash_password, verify_password, create_access_token, verify_access_token
from app.utils.overlaps import calculate_fund_overlaps
from app.utils.metrics import create_data_sets, get_user_investment_data
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# === Authentication Routes ===
@router.post("/register", tags=["Authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/token", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# === JWT Authentication Dependency ===
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload["sub"]

# === Mutual Fund Routes (JWT Protected) ===
@router.get("/mutual-funds", response_model=List[MutualFundResponse], tags=["Mutual Funds"])
def get_mutual_funds(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Fetch all mutual funds (Authenticated)"""
    return db.query(MutualFund).all()

@router.get("/mutual-funds/{fund_id}", response_model=MutualFundResponse, tags=["Mutual Funds"])
def get_mutual_fund(fund_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Fetch details of a specific mutual fund (Authenticated)"""
    fund = db.query(MutualFund).filter(MutualFund.id == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

@router.get("/investments", response_model=List[InvestmentResponse], tags=["Investments"])
def get_investments(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Fetch all investments (Authenticated)"""
    return db.query(Investment).all()

@router.get("/investments/{fund_id}", response_model=List[InvestmentResponse], tags=["Investments"])
def get_investments_by_fund(fund_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Fetch investments for a specific mutual fund (Authenticated)"""
    investments = db.query(Investment).filter(Investment.mutual_fund_id == fund_id).all()
    if not investments:
        raise HTTPException(status_code=404, detail="No investments found for this fund")
    return investments

@router.get("/metrics/", tags=['metrics'])
def get_metrics():
    metrics = create_data_sets()
    return metrics

@router.get("/portfolio_composition/")
def get_portfolio_composition(db: Session = Depends(get_db)):
    # Fetch all investments with mutual fund details
    investment_data = (
        db.query(
            Investment.mutual_fund_id,
            Investment.amount_invested,
            Allocation.sector_allocation
        )
        .join(MutualFund, MutualFund.id == Investment.mutual_fund_id)
        .join(Allocation, Allocation.mutual_fund_id == Investment.mutual_fund_id)
        .all()
    )

    sector_allocation_totals = {}
    total_invested = 0

    # Process investments and compute sector-wise allocation
    for mutual_fund_id, amount_invested, sector_allocation in investment_data:
        total_invested += amount_invested
        sector_allocation_dict = sector_allocation  # Assuming sector_allocation is a dict

        for sector, percentage in sector_allocation_dict.items():
            sector_investment = (amount_invested * percentage) / 100
            if sector in sector_allocation_totals:
                sector_allocation_totals[sector] += sector_investment
            else:
                sector_allocation_totals[sector] = sector_investment

    # Compute percentage allocation for each sector
    portfolio_composition = [
        {
            "sector": sector,
            "amount": round(amount, 2),
            "percentage": round((amount / total_invested) * 100, 2) if total_invested > 0 else 0
        }
        for sector, amount in sector_allocation_totals.items()
    ]

    return {"total_invested": total_invested, "sector_allocation": portfolio_composition}


@router.get("/fund-overlaps/")
def fund_overlaps(db: Session = Depends(get_db)):
    return calculate_fund_overlaps(db)

@router.get("/user-investments/")
def get_user_investments(db: Session = Depends(get_db)):
    return get_user_investment_data(db)
