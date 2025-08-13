import os
import time
from jose import jwt, JWTError
from passlib.hash import bcrypt

SECRET = os.getenv("JWT_SECRET", "devsecret")
ALGO   = os.getenv("JWT_ALGO", "HS256")
EXPIRE = int(os.getenv("JWT_EXPIRE_MIN", "360"))

def hash_password(plain: str) -> str:
    return bcrypt.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_access_token(sub: str ) -> str:
    payload = {"sub": str(sub), "exp": int(time.time()) + EXPIRE*60}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError:
        return None
