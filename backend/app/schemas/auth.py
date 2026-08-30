from pydantic import BaseModel


class RegisterData(BaseModel):
    user_id: str


class RegisterResponse(BaseModel):
    success: bool
    data: RegisterData
    message: str


class LoginUserData(BaseModel):
    id: str
    name: str
    role: str


class LoginData(BaseModel):
    access_token: str
    user: LoginUserData


class LoginResponse(BaseModel):
    success: bool
    data: LoginData
    message: str