"""
TRIE - Sederhananya:
Ini seperti "pohon huruf". Setiap huruf dari nama disimpan sebagai cabang.
Contoh: nama "BUDI" dan "BUDIMAN" akan berbagi cabang B-U-D-I, baru setelah
itu bercabang beda. Ini yang bikin fitur autocomplete/prefix search jadi
sangat cepat: waktu user ngetik "BUD", kita tinggal jalan ke cabang B-U-D
lalu lihat semua nama yang ada di bawahnya.

Kegunaan di aplikasi ini:
- Fitur autocomplete: begitu user mengetik beberapa huruf awal nama,
  aplikasi langsung menyarankan nama-nama yang cocok
"""


class NodeTrie:
    def __init__(self):
        self.anak = {}          # dictionary huruf -> NodeTrie berikutnya
        self.akhir_kata = False  # True kalau di titik ini sebuah nama berakhir


class Trie:
    def __init__(self):
        self.root = NodeTrie()

    def insert(self, kata: str):
        """Memasukkan sebuah nama ke dalam trie, huruf demi huruf."""
        kata = kata.lower()
        node = self.root
        for huruf in kata:
            if huruf not in node.anak:
                node.anak[huruf] = NodeTrie()
            node = node.anak[huruf]
        node.akhir_kata = True

    def _cari_node_prefix(self, prefix: str):
        # Menyusuri trie mengikuti huruf-huruf di prefix
        node = self.root
        for huruf in prefix:
            if huruf not in node.anak:
                return None  # prefix tidak ditemukan sama sekali
            node = node.anak[huruf]
        return node

    def _kumpulkan_semua_kata(self, node, prefix_sekarang, hasil):
        if node.akhir_kata:
            hasil.append(prefix_sekarang)
        for huruf, anak_node in node.anak.items():
            self._kumpulkan_semua_kata(anak_node, prefix_sekarang + huruf, hasil)

    def cari_dengan_awalan(self, prefix: str):
        """
        Fitur AUTOCOMPLETE.
        Mengembalikan semua nama yang diawali dengan `prefix`.
        Contoh: prefix "bu" -> ["budi", "budiman", "bunga"]
        """
        prefix = prefix.lower()
        node_awal = self._cari_node_prefix(prefix)
        if not node_awal:
            return []
        hasil = []
        self._kumpulkan_semua_kata(node_awal, prefix, hasil)
        return hasil

    def hapus(self, kata: str):
        """Menghapus sebuah nama dari trie (dipakai saat kontak dihapus)."""
        kata = kata.lower()
        self._hapus(self.root, kata, 0)

    def _hapus(self, node, kata, kedalaman):
        if kedalaman == len(kata):
            if node.akhir_kata:
                node.akhir_kata = False
            return len(node.anak) == 0  # boleh dihapus kalau tidak punya cabang lain

        huruf = kata[kedalaman]
        if huruf not in node.anak:
            return False

        boleh_hapus_anak = self._hapus(node.anak[huruf], kata, kedalaman + 1)

        if boleh_hapus_anak:
            del node.anak[huruf]
            return len(node.anak) == 0 and not node.akhir_kata

        return False
