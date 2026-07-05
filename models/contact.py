"""
File ini isinya cuma template data buat satu kontak.
"""


class Contact:
    def __init__(self, nama: str, nomor: str, email: str = ""):
        self.nama = nama          # Nama kontak, contoh: "Budi Santoso"
        self.nomor = nomor        # Nomor telepon, contoh: "081234567890"
        self.email = email        # Email (boleh kosong)

    def __repr__(self):
        # Ini cuma buat tampilan pas di-print, biar rapi di layar
        return f"{self.nama} | {self.nomor} | {self.email or '-'}"

    def to_dict(self):
        # Ubah jadi dictionary, berguna waktu mau disimpan ke CSV
        return {"nama": self.nama, "nomor": self.nomor, "email": self.email}
