from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PermissionBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    modulo: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    modulo: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class PermissionResponse(PermissionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoleBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class RoleCreate(RoleBase):
    permission_ids: List[int] = []


class RoleUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    permission_ids: Optional[List[int]] = None


class RoleResponse(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    permissions: List[PermissionResponse] = []


class UserBase(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    estado: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    role_ids: List[int] = []


class UserUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    estado: Optional[bool] = None
    role_ids: Optional[List[int]] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fecha_creacion: datetime
    roles: List[RoleResponse] = []


class UserRegister(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str
