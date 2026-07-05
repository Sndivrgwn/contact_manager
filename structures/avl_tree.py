"""
avl tree itu cara nyimpen kontak dalam bentuk "pohon" yang urut berdasarkan nama,
dan pohon ini "pintar" karena selalu menyeimbangkan dirinya sendiri setiap kali
ada data baru masuk atau dihapus. Karena selalu seimbang, pencarian selalu cepat
yaitu O(log n) - artinya walau datanya jutaan, pencarian tetap kilat.
"""


class NodeAVL:
    """Satu 'kotak' di dalam pohon, isinya key (nama) dan data (objek Contact)."""

    def __init__(self, key, data):
        self.key = key            
        self.data = data         
        self.kiri = None         
        self.kanan = None         
        self.tinggi = 1         


class AVLTree:
    def __init__(self):
        self.root = None


    def _tinggi(self, node):
        return node.tinggi if node else 0

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._tinggi(node.kiri) - self._tinggi(node.kanan)

    def _update_tinggi(self, node):
        node.tinggi = 1 + max(self._tinggi(node.kiri), self._tinggi(node.kanan))

    def _putar_kanan(self, y):
        x = y.kiri
        T2 = x.kanan
        x.kanan = y
        y.kiri = T2
        self._update_tinggi(y)
        self._update_tinggi(x)
        return x

    def _putar_kiri(self, x):
        y = x.kanan
        T2 = y.kiri
        y.kiri = x
        x.kanan = T2
        self._update_tinggi(x)
        self._update_tinggi(y)
        return y


    def insert(self, key, data):
        """Menambahkan kontak baru ke pohon, lalu pohon otomatis menyeimbangkan diri."""
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return NodeAVL(key, data)
        if key < node.key:
            node.kiri = self._insert(node.kiri, key, data)
        elif key > node.key:
            node.kanan = self._insert(node.kanan, key, data)
        else:
            node.data = data
            return node

        self._update_tinggi(node)

        balance = self._balance_factor(node)

        if balance > 1 and key < node.kiri.key:
            return self._putar_kanan(node)
        if balance < -1 and key > node.kanan.key:
            return self._putar_kiri(node)
        if balance > 1 and key > node.kiri.key:
            node.kiri = self._putar_kiri(node.kiri)
            return self._putar_kanan(node)
        if balance < -1 and key < node.kanan.key:
            node.kanan = self._putar_kanan(node.kanan)
            return self._putar_kiri(node)

        return node


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
            if not node.kiri:
                return node.kanan
            if not node.kanan:
                return node.kiri
            pengganti = self._cari_termin(node.kanan)
            node.key = pengganti.key
            node.data = pengganti.data
            node.kanan = self._delete(node.kanan, pengganti.key)

        self._update_tinggi(node)
        balance = self._balance_factor(node)

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
