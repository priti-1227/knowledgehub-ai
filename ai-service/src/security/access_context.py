from dataclasses import dataclass


@dataclass(frozen=True)
class AccessContext:
    """
    Represents the security context of the
    currently authenticated user.
    """

    user_id: int

    department: str | None

    roles: tuple[str, ...] = ()

    is_admin: bool = False