# apis defined
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from .schemas import UserCreate, UserUpdate, User as UserSchema
from .service import autenticate, create_access_token, existing_user, create_user as create_user_svc, get_current_user, update_user as update_user_svc
from database import get_db

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session=Depends(get_db)):
    db_user = await existing_user(username=user.username, email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username or Email already Exist!')
    
    db_user = await create_user_svc(db, user)

    access_token = await create_access_token(username=db_user.username, id=db_user.id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': db_user.username
    }

@router.post('/token', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    db_user = await autenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    
    access_token = await create_access_token(db_user.username, db_user.id)

    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/profile', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def current_user(token: str, db: Session=Depends(get_db)):
    db_user = await get_current_user(db, token)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return db_user

@router.put('/{username}', status_code=status.HTTP_200_OK)
async def update_user(username: str, token: str, user_update: UserUpdate, db: Session=Depends(get_db)):
    db_user = await get_current_user(token=token, db=db)
    if not db_user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized!!!')
    await update_user_svc(db, db_user, user_update)






# Signup
# login to generate token
# get current user
# upodate user