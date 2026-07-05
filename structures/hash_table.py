"""
Hash table itu kan metode key value jadi kita nyimpen key node dan bisa kita pake 
buat cari value yang kita mau. Misalkan saya nyari nomor 08sekian nah hash table 
langsung tau dia disimpen dimana node nya karna udah ada key nya
"""


class HashTable:
    def __init__(self, jumlah_ember: int = 128):
        self.jumlah_ember = jumlah_ember
        self.ember = [[] for _ in range(jumlah_ember)]
        self.jumlah_data = 0

    def _hash(self, key: str) -> int:
        """Fungsi yang mengubah nomor telepon jadi nomor ember(key nya hashtable)."""
        return sum(ord(karakter) for karakter in key) % self.jumlah_ember

    def set(self, key: str, value):
        """Menyimpan/mengganti data kontak berdasarkan nomor telepon."""
        index = self._hash(key)
        bucket = self.ember[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # nomor sudah ada, update datanya
                return
        bucket.append((key, value))
        self.jumlah_data += 1

    def get(self, key: str):
        """Mengambil data kontak berdasarkan nomor telepon. None kalau tidak ketemu."""
        index = self._hash(key)
        for k, v in self.ember[index]:
            if k == key:
                return v
        return None

    def contains(self, key: str) -> bool:
        """Cek apakah nomor telepon sudah terdaftar."""
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """Menghapus data kontak berdasarkan nomor telepon."""
        index = self._hash(key)
        bucket = self.ember[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.jumlah_data -= 1
                return True
        return False

    def semua_value(self):
        """Ambil semua data kontak yang tersimpan (dari semua ember)."""
        hasil = []
        for bucket in self.ember:
            for _, v in bucket:
                hasil.append(v)
        return hasil
