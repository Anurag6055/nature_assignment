from sqlalchemy.orm import Session
import database, config
from datetime import datetime, timedelta
import random

# Helper funtions

def generate_short_code(db: Session) -> str:
    """Returns a short 6 characters code"""
    for i in range(config.settings.CODE_LENGTH):
        code = ''.join(random.choice(config.settings.CODE_CHARACTERS) for _ in range(config.settings.CODE_LENGTH))
        exists = db.query(database.URLMap).filter_by(short_code = code).first()
        if not exists:
            return code

def create_short_url(db: Session, url: str, alias: str = None, expiry: int = None):
    if alias:
        if db.query(database.URLMap).filter_by(short_code=alias).first():
            return None, "Alias is already being used"
        short_code = alias
    else:
        short_code = generate_short_code(db)

    expires_at = datetime.utcnow() + timedelta(seconds=expiry) if expiry else None

    new_item = database.URLMap(
        long_url = url,
        short_code = short_code,
        expires_at = expires_at
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item, None