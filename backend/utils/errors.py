from fastapi import HTTPException, status


def not_found(detail: str) -> HTTPException:
    """Create a standardized not found error."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def unauthorized(detail: str) -> HTTPException:
    """Create a standardized unauthorized error."""
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def forbidden(detail: str) -> HTTPException:
    """Create a standardized forbidden error."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def bad_request(detail: str) -> HTTPException:
    """Create a standardized bad request error."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
