# File: main.py

from fastapi import FastAPI
from api import predict

# --- TAMBAHKAN BAGIAN INI ---
from database import engine
from models import user, history

# Baris ini akan memerintahkan SQLAlchemy untuk membuat semua tabel
# yang didefinisikan di dalam model (user.py dan history.py)
# ke dalam database MySQL Anda jika tabel-tabel tersebut belum ada.
user.Base.metadata.create_all(bind=engine)
history.Base.metadata.create_all(bind=engine)
# ---------------------------

app = FastAPI(
    title="GuavaScan API",
    description="API untuk mendeteksi penyakit pada jambu biji dengan struktur modular."
)

# ... sisa kode Anda ...