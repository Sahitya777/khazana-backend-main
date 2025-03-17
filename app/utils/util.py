import os
from datetime import datetime, timedelta
from typing import Dict
from passlib.context import CryptContext
from jose import JWTError, jwt

# Load secret key from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === 🔑 Password Hashing Functions ===
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# === 🔐 JWT Token Functions ===
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generate a JWT access token.
    :param data: Dictionary containing user data.
    :param expires_delta: Expiration duration for the token.
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    """
    Verify and decode a JWT access token.
    :param token: JWT token string.
    :return: Decoded payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Returns user details (e.g., {"sub": "username"})
    except JWTError:
        return None

# === 📈 Mutual Fund Utility Functions ===
def calculate_return_percentage(initial_nav: float, current_nav: float) -> float:
    """
    Calculate returns since investment as a percentage.
    Formula: ((Current NAV - Initial NAV) / Initial NAV) * 100
    """
    return round(((current_nav - initial_nav) / initial_nav) * 100, 2)

def calculate_stock_overlap(fund1: Dict[str, float], fund2: Dict[str, float]) -> float:
    """
    Calculate stock overlap percentage between two mutual funds.
    Overlap = sum of minimum percentages of shared stocks in both funds.
    """
    common_stocks = set(fund1.keys()) & set(fund2.keys())
    overlap_percentage = sum(min(fund1[stock], fund2[stock]) for stock in common_stocks)
    return round(overlap_percentage, 2)
