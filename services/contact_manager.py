"""
CONTACT MANAGER - Ini adalah "otak" dari aplikasi.
File ini menggabungkan ketiga struktur data (AVL Tree, Hash Table, Trie)
supaya bekerja bersama-sama setiap kali ada kontak ditambah, dicari,
diubah, atau dihapus. GUI (tampilan) tidak perlu tahu detail rumit
struktur data, cukup panggil fungsi-fungsi di file ini.

Catatan asumsi sederhana untuk keperluan tugas:
- Nama kontak dianggap unik (jadi key utama di AVL Tree & Trie)
- Nomor telepon juga dianggap unik (jadi key utama di Hash Table)
"""

import csv
import os

from models.contact import Contact
from structures.avl_tree import AVLTree
from structures.hash_table import HashTable
from structures.trie import Trie
from utils.validators import validasi_nama, validasi_nomor, validasi_email


class ContactManager:
    def __init__(self):
        self.avl = AVLTree()            # menyimpan kontak terurut berdasarkan nama
        self.hash_table = HashTable()   # menyimpan kontak berdasarkan nomor telepon
        self.trie = Trie()              # menyimpan nama untuk fitur autocomplete
        self.trie_nomor = Trie()        # menyimpan nomor telepon untuk pencarian awalan (mis. "0815")

    # ---------- CREATE ----------

    def tambah_kontak(self, nama: str, nomor: str, email: str = ""):
        """
        Menambahkan kontak baru ke SEMUA struktur data sekaligus.
        Mengembalikan (True, pesan) kalau berhasil, (False, pesan) kalau gagal.
        """
        nama = nama.strip()
        nomor = nomor.strip()
        email = email.strip()

        if not validasi_nama(nama):
            return False, "Nama tidak valid (minimal 2 huruf)."
        if not validasi_nomor(nomor):
            return False, "Nomor telepon tidak valid (harus 8-15 digit angka)."
        if not validasi_email(email):
            return False, "Format email tidak valid."
        if self.hash_table.contains(nomor):
            return False, f"Nomor {nomor} sudah terdaftar."
        if self.avl.search(nama.lower()):
            return False, f"Nama '{nama}' sudah terdaftar."

        kontak = Contact(nama, nomor, email)

        # Masukkan ke tiga-tiganya sekaligus
        self.avl.insert(nama.lower(), kontak)
        self.hash_table.set(nomor, kontak)
        self.trie.insert(nama)
        self.trie_nomor.insert(nomor)

        return True, f"Kontak '{nama}' berhasil ditambahkan."

    # ---------- READ ----------

    def cari_berdasarkan_nama(self, nama: str):
        """Cari kontak lewat nama, memakai AVL Tree -> cepat, O(log n)."""
        return self.avl.search(nama.strip().lower())

    def cari_berdasarkan_nomor(self, nomor: str):
        """Cari kontak lewat nomor telepon, memakai Hash Table -> instan, O(1)."""
        return self.hash_table.get(nomor.strip())

    def autocomplete_nama(self, prefix: str):
        """Sarankan nama-nama yang diawali huruf tertentu, memakai Trie -> O(m)."""
        if not prefix:
            return []
        return self.trie.cari_dengan_awalan(prefix.strip())

    def cari_nama_awalan(self, prefix: str):
        """
        PENCARIAN AWALAN NAMA (prefix search).
        Contoh: ketik "wahyu" -> muncul SEMUA kontak yang namanya diawali
        "wahyu", misalnya "Wahyu A", "Wahyu B", dst.
        Caranya: Trie mencari semua nama yang cocok awalannya (cepat, O(m)),
        lalu tiap nama itu dicocokkan ke AVL Tree untuk ambil data lengkapnya.
        """
        prefix = prefix.strip()
        if not prefix:
            return []
        daftar_nama = self.trie.cari_dengan_awalan(prefix)
        hasil = []
        for nama in daftar_nama:
            kontak = self.avl.search(nama)  # nama dari trie sudah huruf kecil
            if kontak:
                hasil.append(kontak)
        hasil.sort(key=lambda k: k.nama.lower())
        return hasil

    def cari_nomor_awalan(self, prefix: str):
        """
        PENCARIAN AWALAN NOMOR TELEPON (prefix search).
        Contoh: ketik "0815" -> muncul SEMUA kontak yang nomornya diawali "0815".
        Memakai Trie kedua (trie_nomor) yang isinya digit-digit nomor telepon,
        jadi walau ada ribuan kontak, pencarian tetap cepat -> O(m).
        """
        prefix = prefix.strip()
        if not prefix:
            return []
        daftar_nomor = self.trie_nomor.cari_dengan_awalan(prefix)
        hasil = []
        for nomor in daftar_nomor:
            kontak = self.hash_table.get(nomor)
            if kontak:
                hasil.append(kontak)
        hasil.sort(key=lambda k: k.nomor)
        return hasil

    def semua_kontak_terurut(self):
        """Ambil semua kontak, sudah terurut A-Z (hasil in-order traversal AVL Tree)."""
        return self.avl.inorder()

    # ---------- UPDATE ----------

    def update_kontak(self, nomor_lama: str, nama_baru: str, nomor_baru: str, email_baru: str = ""):
        """
        Mengubah data kontak. Caranya: hapus data lama dari 3 struktur,
        lalu tambahkan lagi data yang baru (lebih sederhana daripada
        mengubah tiap struktur satu-satu).
        """
        kontak_lama = self.hash_table.get(nomor_lama)
        if not kontak_lama:
            return False, "Kontak dengan nomor tersebut tidak ditemukan."

        nama_lama = kontak_lama.nama

        # Hapus dulu data lama
        self.hapus_kontak(nomor_lama)

        # Coba tambahkan data baru
        berhasil, pesan = self.tambah_kontak(nama_baru, nomor_baru, email_baru)

        if not berhasil:
            # Kalau gagal update, kembalikan data lama supaya tidak hilang
            self.tambah_kontak(nama_lama, nomor_lama, kontak_lama.email)
            return False, pesan

        return True, "Kontak berhasil diperbarui."

    # ---------- DELETE ----------

    def hapus_kontak(self, nomor: str):
        """Menghapus kontak dari SEMUA struktur data sekaligus, berdasarkan nomor telepon."""
        kontak = self.hash_table.get(nomor)
        if not kontak:
            return False, "Kontak tidak ditemukan."

        self.hash_table.delete(nomor)
        self.avl.delete(kontak.nama.lower())
        self.trie.hapus(kontak.nama)
        self.trie_nomor.hapus(kontak.nomor)

        return True, f"Kontak '{kontak.nama}' berhasil dihapus."

    # ---------- IMPORT / EXPORT CSV ----------

    def ekspor_csv(self, path_file: str):
        """Menyimpan semua kontak ke file CSV, supaya bisa dibuka di Excel dll."""
        kontak_list = self.semua_kontak_terurut()
        with open(path_file, mode="w", newline="", encoding="utf-8") as f:
            penulis = csv.DictWriter(f, fieldnames=["nama", "nomor", "email"])
            penulis.writeheader()
            for kontak in kontak_list:
                penulis.writerow(kontak.to_dict())
        return True, f"{len(kontak_list)} kontak berhasil diekspor ke {path_file}"

    def impor_csv(self, path_file: str):
        """Membaca file CSV dan menambahkan tiap barisnya sebagai kontak baru."""
        if not os.path.exists(path_file):
            return False, "File tidak ditemukan."

        jumlah_sukses = 0
        jumlah_gagal = 0
        with open(path_file, mode="r", newline="", encoding="utf-8") as f:
            pembaca = csv.DictReader(f)
            for baris in pembaca:
                nama = baris.get("nama", "")
                nomor = baris.get("nomor", "")
                email = baris.get("email", "")
                berhasil, _ = self.tambah_kontak(nama, nomor, email)
                if berhasil:
                    jumlah_sukses += 1
                else:
                    jumlah_gagal += 1

        return True, f"Impor selesai: {jumlah_sukses} berhasil, {jumlah_gagal} gagal/dilewati."
