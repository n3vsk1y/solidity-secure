async def valid_email_from_db(email: str) -> bool:
    return True


async def add_blacklist_token(token: str) -> bool:
    return True


async def is_token_blacklisted(token: str) -> bool:
    return False
