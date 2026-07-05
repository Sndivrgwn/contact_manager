"""
AVL TREE - Sederhananya:
Ini adalah cara menyimpan kontak dalam bentuk "pohon" yang urut berdasarkan nama,
dan pohon ini "pintar" karena selalu menyeimbangkan dirinya sendiri setiap kali
ada data baru masuk atau dihapus. Karena selalu seimbang, pencarian selalu cepat
yaitu O(log n) - artinya walau datanya jutaan, pencarian tetap kilat.

Kegunaan di aplikasi ini:
- Menyimpan kontak terurut berdasarkan nama (A-Z)
- Mencari kontak berdasarkan nama dengan cepat
- Menampilkan semua kontak secara terurut alfabetis
"""


class NodeAVL:
    """Satu 'kotak' di dalam pohon, isinya key (nama) dan data (objek Contact)."""

    def __init__(self, key, data):
        self.key = key            # nama kontak, dipakai untuk mengurutkan
        self.data = data          # objek Contact yang sesungguhnya
        self.kiri = None          # anak sebelah kiri (nama lebih kecil)
        self.kanan = None         # anak sebelah kanan (nama lebih besar)
        self.tinggi = 1           # tinggi node, dipakai untuk cek keseimbangan


class AVLTree:
    def __init__(self):
        self.root = None

    # ---------- FUNGSI BANTUAN (rumus keseimbangan) ----------

    def _tinggi(self, node):
        # Kalau node kosong, tingginya 0
        return node.tinggi if node else 0

    def _balance_factor(self, node):
        # Selisih tinggi kiri dan kanan. Kalau lebih dari 1 atau kurang dari -1,
        # berarti pohon "miring" dan perlu diseimbangkan lagi
        if not node:
            return 0
        return self._tinggi(node.kiri) - self._tinggi(node.kanan)

    def _update_tinggi(self, node):
        node.tinggi = 1 + max(self._tinggi(node.kiri), self._tinggi(node.kanan))

    def _putar_kanan(self, y):
        # "Putar" node ke kanan supaya pohon jadi seimbang lagi
        x = y.kiri
        T2 = x.kanan
        x.kanan = y
        y.kiri = T2
        self._update_tinggi(y)
        self._update_tinggi(x)
        return x

    def _putar_kiri(self, x):
        # "Putar" node ke kiri supaya pohon jadi seimbang lagi
        y = x.kanan
        T2 = y.kiri
        y.kiri = x
        x.kanan = T2
        self._update_tinggi(x)
        self._update_tinggi(y)
        return y

    # ---------- INSERT ----------

    def insert(self, key, data):
        """Menambahkan kontak baru ke pohon, lalu pohon otomatis menyeimbangkan diri."""
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        # Langkah 1: masukkan seperti binary search tree biasa
        if not node:
            return NodeAVL(key, data)
        if key < node.key:
            node.kiri = self._insert(node.kiri, key, data)
        elif key > node.key:
            node.kanan = self._insert(node.kanan, key, data)
        else:
            # nama sudah ada, update datanya saja
            node.data = data
            return node

        # Langkah 2: update tinggi node ini
        self._update_tinggi(node)

        # Langkah 3: cek keseimbangan, putar kalau perlu
        balance = self._balance_factor(node)

        # Kasus miring ke kiri
        if balance > 1 and key < node.kiri.key:
            return self._putar_kanan(node)
        # Kasus miring ke kanan
        if balance < -1 and key > node.kanan.key:
            return self._putar_kiri(node)
        # Kasus kiri-kanan
        if balance > 1 and key > node.kiri.key:
            node.kiri = self._putar_kiri(node.kiri)
            return self._putar_kanan(node)
        # Kasus kanan-kiri
        if balance < -1 and key < node.kanan.key:
            node.kanan = self._putar_kanan(node.kanan)
            return self._putar_kiri(node)

        return node

    # ---------- SEARCH ----------

    def search(self, key):
        """Mencari kontak berdasarkan nama. Cepat karena pohonnya seimbang."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.data
        if key < node.key:
            return self._search(node.kiri, key)
        return self._search(node.kanan, key)

    # ---------- DELETE ----------

    def delete(self, key):
        """Menghapus kontak berdasarkan nama, lalu pohon menyeimbangkan diri lagi."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return None

        if key < node.key:
            node.kiri = self._delete(node.kiri, key)
        elif key > node.key:
            node.kanan = self._delete(node.kanan, key)
        else:
            # Node ditemukan, ini yang mau dihapus
            if not node.kiri:
                return node.kanan
            if not node.kanan:
                return node.kiri
            # Punya dua anak: cari pengganti terkecil di subtree kanan
            pengganti = self._cari_termin(node.kanan)
            node.key = pengganti.key
            node.data = pengganti.data
            node.kanan = self._delete(node.kanan, pengganti.key)

        self._update_tinggi(node)
        balance = self._balance_factor(node)

        # Seimbangkan lagi kalau perlu (sama seperti waktu insert)
        if balance > 1 and self._balance_factor(node.kiri) >= 0:
            return self._putar_kanan(node)
        if balance > 1 and self._balance_factor(node.kiri) < 0:
            node.kiri = self._putar_kiri(node.kiri)
            return self._putar_kanan(node)
        if balance < -1 and self._balance_factor(node.kanan) <= 0:
            return self._putar_kiri(node)
        if balance < -1 and self._balance_factor(node.kanan) > 0:
            node.kanan = self._putar_kanan(node.kanan)
            return self._putar_kiri(node)

        return node

    def _cari_termin(self, node):
        # Cari node paling kiri (nilai terkecil) di sebuah subtree
        while node.kiri:
            node = node.kiri
        return node

    # ---------- TRAVERSAL ----------

    def inorder(self):
        """Mengembalikan semua kontak terurut A-Z berdasarkan nama."""
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.kiri, hasil)
            hasil.append(node.data)
            self._inorder(node.kanan, hasil)
