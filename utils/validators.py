"""
File ini isinya "satpam" yang mengecek apakah data yang dimasukkan
user itu masuk akal atau tidak, sebelum disimpan ke sistem.
"""

import re


def validasi_nomor(nomor: str) -> bool:
    """
    Cek apakah nomor telepon valid:
    - hanya boleh angka (boleh diawali tanda +)
    - panjang antara 8 sampai 15 digit
    Contoh valid   : 081234567890, +6281234567890
    Contoh tidak   : abc123, 123
    """
    if not nomor:
        return False
    pola = r"^\+?[0-9]{8,15}$"
    return re.match(pola, nomor) is not None


def validasi_nama(nama: str) -> bool:
    """
    Cek apakah nama valid: tidak boleh kosong dan minimal 2 huruf.
    """
    return bool(nama) and len(nama.strip()) >= 2


def validasi_email(email: str) -> bool:
    """
    Cek format email sederhana. Email boleh kosong (opsional),
    tapi kalau diisi harus mengikuti pola standar.
    """
    if not email:
        return True  # email opsional, boleh kosong
    pola = r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
    return re.match(pola, email) is not None
