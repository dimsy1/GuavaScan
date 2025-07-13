# ===================================================================
# File: history.py
# Lokasi: GuavaScan/Backend/api/history.py
# Deskripsi: Endpoint API untuk mengelola riwayat pemindaian pengguna,
#            termasuk mengambil dan menghapus data riwayat.
# ===================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import history as history_model
from schemas import history_schema
from services import auth_service
from database import SessionLocal

# Membuat instance router baru untuk dikelompokkan
router = APIRouter()

# Dependency untuk mendapatkan sesi database pada setiap permintaan
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mengimpor dependency get_current_user dari file predict.py
# untuk memastikan hanya pengguna yang sudah login yang bisa mengakses endpoint ini.
# Titik di depan (.predict) menandakan impor dari file dalam direktori yang sama.
from .predict import get_current_user 

@router.get("/", response_model=List[history_schema.HistoryResponse])
def get_user_history(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user)
):
    """
    Endpoint untuk mengambil semua riwayat pemindaian milik pengguna yang sedang login.
    Mengembalikan daftar riwayat yang cocok dengan id_pengguna dari token.
    """
    history = db.query(history_model.RiwayatPindai).filter(history_model.RiwayatPindai.id_pengguna == current_user_id).all()
    return history

@router.delete("/{history_id}")
def delete_user_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    Endpoint untuk menghapus satu entri riwayat pemindaian berdasarkan ID-nya.
    """
    # Mencari data riwayat yang akan dihapus di database.
    # Query ini memiliki dua kondisi:
    # 1. ID riwayat harus cocok.
    # 2. ID pengguna pada riwayat tersebut harus cocok dengan ID pengguna yang sedang login.
    # Ini untuk memastikan pengguna tidak bisa menghapus riwayat milik orang lain.
    history_to_delete = db.query(history_model.RiwayatPindai).filter(
        history_model.RiwayatPindai.id_riwayat == history_id,
        history_model.RiwayatPindai.id_pengguna == current_user_id
    ).first()

    # Jika data riwayat tidak ditemukan, kirim error 404 Not Found.
    if not history_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Riwayat tidak ditemukan atau Anda tidak memiliki akses.")
    
    # Jika ditemukan, hapus data tersebut dari database.
    db.delete(history_to_delete)
    db.commit()
    
    return {"message": "Riwayat berhasil dihapus"}
