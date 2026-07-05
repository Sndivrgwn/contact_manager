"""
TRIE kita pake buat nyari nama yang efektif jadi kalau kita mau 
nyari user dengan nama wahyu kita cuma perlu ngetik wah dan langsung
muncul semua user yang berawalan wah
"""


class NodeTrie:
    def __init__(self):
        self.anak = {}          
        self.akhir_kata = False  


class Trie:
    def __init__(self):
        self.root = NodeTrie()

    def insert(self, kata: str):
        """Memasukkan semua nama ke dalam trie."""
        kata = kata.lower()
        node = self.root
        for huruf in kata:
            if huruf not in node.anak:
                node.anak[huruf] = NodeTrie()
            node = node.anak[huruf]
        node.akhir_kata = True

    def _cari_node_prefix(self, prefix: str):
        node = self.root
        for huruf in prefix:
            if huruf not in node.anak:
                return None  
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
