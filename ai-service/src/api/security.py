import os

from fastapi import (
    Header,
    HTTPException,
    status,
)


SERVICE_API_KEY = os.getenv(
    "AI_SERVICE_API_KEY"
)


def verify_service_api_key(
    x_service_api_key: str | None = Header(
        default=None
    ),
) -> None:
    """
    Verify that the request came from an
    authorized internal service.
    """

    if not SERVICE_API_KEY:
        raise RuntimeError(
            "AI_SERVICE_API_KEY is not configured."
        )

    if x_service_api_key != SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service credentials.",
        )