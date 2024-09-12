from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .models import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='v1/auth/token')
SECRETE_KEY = 'secret_key'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 30

# check for existing user
async def existing_user(db: Session, username: str, email: str):
    return db.query(User).filter(or_(User.username == username, User.email == email)).first()

# create access token
async def create_access_token(username: str, id: int):
    encode = {'sub': username, 'id': id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRETE_KEY, algorithm=ALGORITHM)

# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id:int = payload.get('id')
        expires: datetime = payload.get('exp')
        if datetime(expires) < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).filter()
    except JWTError:
        return None

# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()