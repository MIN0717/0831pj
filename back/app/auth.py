import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

from jwt.exceptions import InvalidTokenError

from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)

from pwdlib import PasswordHash

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.redis_client import redis_client


# =========================================================
# ENV
# =========================================================

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(ENV_PATH)


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-secret-key",
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30",
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7",
    )
)


# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# =========================================================
# Security
# =========================================================

bearer_scheme = HTTPBearer(
    auto_error=False,
)

password_hash = PasswordHash.recommended()


# =========================================================
# Schemas
# =========================================================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    email: str
    nickname: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# =========================================================
# Password
# =========================================================

def hash_password(
    password: str,
) -> str:

    return password_hash.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


# =========================================================
# Access Token
# =========================================================

def create_access_token(
    user_id: int,
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


# =========================================================
# Refresh Token
# =========================================================

def create_refresh_token() -> str:

    return secrets.token_urlsafe(
        64
    )


def save_refresh_token(
    refresh_token: str,
    user_id: int,
) -> None:

    expire_seconds = (
        REFRESH_TOKEN_EXPIRE_DAYS
        * 24
        * 60
        * 60
    )

    redis_client.setex(
        f"refresh:{refresh_token}",
        expire_seconds,
        str(user_id),
    )


def delete_refresh_token(
    refresh_token: str,
) -> int:

    return redis_client.delete(
        f"refresh:{refresh_token}"
    )


def get_refresh_token_user_id(
    refresh_token: str,
) -> int | None:

    user_id = redis_client.get(
        f"refresh:{refresh_token}"
    )

    if user_id is None:
        return None

    try:
        return int(user_id)

    except ValueError:
        return None


# =========================================================
# Current User
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    if credentials is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[
                JWT_ALGORITHM
            ],
        )

        token_type = payload.get(
            "type"
        )

        if token_type != "access":

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Token이 아닙니다.",
            )

        user_id = payload.get(
            "sub"
        )

        if user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )

        user_id = int(
            user_id
        )

    except InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 토큰입니다.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
        )


    user = db.get(
        User,
        user_id,
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )

    return user


# =========================================================
# Signup
# =========================================================

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db),
):

    existing_user = db.scalar(
        select(User).where(
            User.email
            == str(data.email)
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 이메일입니다.",
        )


    user = User(
        email=str(data.email),
        password_hash=hash_password(
            data.password
        ),
        nickname=data.nickname,
    )


    db.add(
        user
    )

    db.commit()

    db.refresh(
        user
    )


    return user


# =========================================================
# Login
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    user = db.scalar(
        select(User).where(
            User.email
            == str(data.email)
        )
    )


    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )


    if not verify_password(
        data.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )


    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )


    access_token = create_access_token(
        user.id
    )


    refresh_token = create_refresh_token()


    save_refresh_token(
        refresh_token,
        user.id,
    )


    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# =========================================================
# Me
# =========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return current_user


# =========================================================
# Refresh
# =========================================================

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_access_token(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):

    user_id = get_refresh_token_user_id(
        data.refresh_token
    )


    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 Refresh Token입니다.",
        )


    user = db.get(
        User,
        user_id,
    )


    if user is None:

        delete_refresh_token(
            data.refresh_token
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
        )


    if not user.is_active:

        delete_refresh_token(
            data.refresh_token
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )


    # 기존 Refresh Token 삭제
    delete_refresh_token(
        data.refresh_token
    )


    # 새로운 Refresh Token 생성
    new_refresh_token = create_refresh_token()


    save_refresh_token(
        new_refresh_token,
        user.id,
    )


    # 새로운 Access Token 생성
    new_access_token = create_access_token(
        user.id
    )


    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


# =========================================================
# Logout
# =========================================================

@router.post(
    "/logout",
)
def logout(
    data: LogoutRequest,
):

    deleted = delete_refresh_token(
        data.refresh_token
    )


    if deleted == 0:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이미 로그아웃되었거나 유효하지 않은 Refresh Token입니다.",
        )


    return {
        "message": "로그아웃되었습니다."
    }