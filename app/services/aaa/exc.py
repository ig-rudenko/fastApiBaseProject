from fastapi import HTTPException
from starlette import status

UserNotActiveException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User not active",
)
CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
InvalidRefreshTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
    headers={"WWW-Authenticate": "Bearer"},
)
InvalidAccessTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid access token",
    headers={"WWW-Authenticate": "Bearer"},
)
