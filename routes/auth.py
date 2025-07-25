from fastapi import APIRouter, Depends, HTTPException, status, Body
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import os

from models.user import User
from database.db import SessionLocal
from schemas.auth import CreateUser, UserReponseCreated, Token, LoginRequest

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    include_in_schema=True
)

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token/form")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str, db: db_dependency):
    user= db.query(User).filter(User.username==username).first()
    
    if not user:
        return False
    
    if not bycrypt_context.verify(password, user.password):
        return False
    
    return user

def create_access_token(username:str, user_id:int, is_admin:bool, expires_delta:timedelta):
    token_encode = {
        'username': username,
        'id': user_id,
        'is_admin': is_admin
    }
    
    expires = datetime.now(timezone.utc) + expires_delta
    token_encode.update({'exp': expires})
    
    return jwt.encode(token_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
        username = payload.get('username')
        user_id = payload.get('id')
        is_admin = payload.get('is_admin')
                
        if username is None or user_id is None or is_admin is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': 'User not authorized.',
                'success': False,
                'data': []
            })
        
        return {'username': username, 'user_id': user_id, 'is_admin': is_admin}
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': 'User not authorized.',
                'success': False,
                'data': []
            })

user_dependecy = Annotated[dict, Depends(get_current_user)]
    
@router.post('/', status_code=status.HTTP_201_CREATED, include_in_schema=True, response_model=UserReponseCreated)
async def create_user(db: db_dependency, user_depen: user_dependecy, user_body : CreateUser = Body(..., examples=CreateUser.Config.json_schema_extra['example'])):
    
    if user_depen is None or user_depen.get('is_admin') != True:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= {
                'message':"user does not have permissions to create User.",
                'succcess':False,
                'data':[]
                })
    
    user_db = db.query(User).filter((User.username == user_body.username) | (User.mail == user_body.mail)).first()
    
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                'message': 'Username o Mail already exist',
                'success': False,
                'data': []
            })
    
    user = User(
        username = user_body.username,
        mail = user_body.mail,
        first_name = user_body.first_name,
        last_name = user_body.last_name,
        is_admin = user_body.is_admin,
        password = bycrypt_context.hash(user_body.password),
        created_datetime = datetime.now(),
        updated_datetime = datetime.now()
    )
    
    try:
        db.add(user)
        db.commit()
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                'message': f'User not created, error: {e}',
                'success': False,
                'data': []
            })
    

@router.post('/token/form', response_model=Token, include_in_schema=False)
async def login_for_access_token_form(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message':"User not authorized.",
            'succcess':False,
            'data':[]
            })
    
    token=create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=60))
    return {'access_token':token, 'token_type':'bearer'}

@router.post('/token', response_model=Token)
async def login_for_access_token( db: db_dependency, login_data: LoginRequest = Body(..., examples=LoginRequest.Config.json_schema_extra['example'])):
    user = authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': "User not authorized.",
                'succcess': False,
                'data': []
            }
        )

    token = create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer'}
