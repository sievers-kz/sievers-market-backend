from pydantic import BaseModel, EmailStr


class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class ForgotPasswordDTO(BaseModel):
    email: EmailStr


class LoginResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
