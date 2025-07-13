# ===================================================================
# File: user_schema.py
# Lokasi: GuavaScan/Backend/schemas/user_schema.py
# Deskripsi: Skema Pydantic untuk validasi data pengguna yang masuk dan keluar dari API.
# ===================================================================

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """
    Skema untuk data yang diterima dari pengguna saat mendaftar.
    Pydantic akan otomatis memvalidasi bahwa 'email' adalah format email yang valid.
    """
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Skema untuk data pengguna yang dikirim kembali sebagai respons dari API.
    Perhatikan bahwa kolom 'password' sengaja tidak disertakan di sini
    untuk alasan keamanan.
    """
    id_pengguna: int
    username: str
    email: EmailStr
    tanggal_dibuat: datetime

    class Config:
        # Konfigurasi ini memungkinkan Pydantic untuk membaca data
        # langsung dari objek model SQLAlchemy (orm_mode).
        # Di Pydantic v2, ini menjadi from_attributes = True.
        orm_mode = True

class Token(BaseModel):
    """
    Skema untuk respons token yang diberikan setelah login berhasil.
    """
    access_token: str
    token_type: str
