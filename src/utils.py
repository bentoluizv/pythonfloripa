from ulid import ULID


def generate_ulid() -> str:
    return str(ULID())


def validade_password(password: str) -> str:
    if not any(c.isalpha() for c in password):
        raise ValueError('Password must contain at least one letter')
    if not any(c.isdigit() for c in password):
        raise ValueError('Password must contain at least one number')
    if not all(c.isalnum() or c in '@$!%*#?&' for c in password):
        raise ValueError('Password can only contain letters, numbers, and @$!%*#?&')
    return password
