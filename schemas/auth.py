from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    username:str
    mail:str
    first_name:str
    last_name:str
    password:str=Field(min_length=6)
    is_admin:bool
    
    class Config:
        json_schema_extra={
            "example": {
                "username": "User",
                "mail": "yourmail@gmail.com",
                "first_name": "Name",
                "last_name": "Last Name",
                "password" : "pass",
                "is_admin": True
            }
        }

class UserReponseCreated(BaseModel):
    username:str
    mail:str
    first_name:str
    last_name:str
    is_admin:bool
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str
    
    class Config:
        json_schema_extra={
            "example":{
                "access_token":"token obtenido",
                "token_type":"tipo de token"
            }
        }

class LoginRequest(BaseModel):
    username: str
    password: str
    
    class Config:
        json_schema_extra={
            "example":{
                "username":"USERNAME",
                "password":"PASSWORD_USER"
            }
        }
