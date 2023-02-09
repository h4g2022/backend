from fastapi import HTTPException, status


class AppError:
    EMAIL_NOT_VALID_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format",
        headers={"WWW-Authenticate": "Bearer"},
    )

    CREDENTIALS_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    USERNAME_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Credentials already exist",
        headers={"WWW-Authenticate": "Bearer"},
    )

    ITEM_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Item already exist",
        headers={"WWW-Authenticate": "Bearer"},
    )

    WRONG_PASSWORD_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    WRONG_USER_TYPE_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect user type",
        headers={"WWW-Authenticate": "Bearer"},
    )

    TALENT_NOT_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Talent does not exist",
        headers={"WWW-Authenticate": "Bearer"},
    )

    LISTING_NOT_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Listing does not exist",
        headers={"WWW-Authenticate": "Bearer"},
    )

    NO_PERMISSION_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No permission to perform this action",
        headers={"WWW-Authenticate": "Bearer"},
    )
