from fastapi import HTTPException, status


class AppError:

    CREDENTIALS_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    USERNAME_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Credentials already exists.",
        headers={"WWW-Authenticate": "Bearer"},
    )
