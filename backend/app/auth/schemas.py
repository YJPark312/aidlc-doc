from pydantic import BaseModel


class RegisterRequest(BaseModel):
    store_name: str
    username: str
    password: str


class LoginRequest(BaseModel):
    store_name: str
    username: str
    password: str


class TableLoginRequest(BaseModel):
    store_id: int
    table_number: int
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    store_id: int
    store_name: str
    user_id: int
    username: str
