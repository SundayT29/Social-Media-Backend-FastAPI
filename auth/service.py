from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth.schemas import UserCreate, UserUpdate
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
        if datetime.fromtimestamp(expires) < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).filter().first()
    except JWTError:
        return None

# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# create user
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email.lower().strip(),
        username=user.username.casefold().strip(),
        hashed_password=bcrypt_context.hash(user.password),
        dob=user.dob or None,
        bio=user.bio or None,
        location=user.location or None,
        profile_pic=user.profile_pic or None,
        name=user.name or None
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

async def autenticate(db:Session, username:str, password:str):
    db_user = await existing_user(db, username, '')
    if not db_user:
        return False
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return False
    return db_user

async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.bio = user_update.bio
    db_user.name = user_update.name
    db_user.dob = user_update.dob
    db_user.gender = user_update.gender
    db_user.location = user_update.location
    db_user.profile_pic = user_update.profile_pic

    db.commit()
