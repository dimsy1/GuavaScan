# ===================================================================
# File: history.py
# Lokasi: GuavaScan/Backend/models/history.py
# Deskripsi: Model data SQLAlchemy untuk tabel 'riwayat_pindai'.
# ===================================================================

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base # Mengimpor Base dari file database.py

class RiwayatPindai(Base):
    """
    Kelas model ini merepresentasikan tabel 'riwayat_pindai' di dalam database.
    Setiap baris pada tabel ini adalah satu catatan hasil pemindaian yang
    dilakukan oleh seorang pengguna.
    """
    __tablename__ = "riwayat_pindai"

    # Mendefinisikan kolom-kolom pada tabel
    id_riwayat = Column(Integer, primary_key=True, index=True)
    
    # Kolom ini adalah Foreign Key yang menghubungkan setiap riwayat
    # dengan pengguna yang melakukannya.
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=False)
    
    # Menyimpan path atau URL ke gambar yang dipindai.
    gambar_pindai = Column(String(255), nullable=False)
    
    hasil_diagnosis = Column(String(255), nullable=False)
    skor_keyakinan = Column(Float, nullable=False)
    
    # Menggunakan String dengan panjang lebih besar untuk menampung teks rekomendasi.
    rekomendasi_penanganan = Column(String(1024))
    
    # Kolom ini akan secara otomatis diisi dengan tanggal dan waktu saat
    # pemindaian dilakukan.
    tanggal_pindai = Column(DateTime(timezone=True), server_default=func.now())

