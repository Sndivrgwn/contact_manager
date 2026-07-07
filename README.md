# Sistem Manajemen Kontak Telepon (Kelompok 5)

Aplikasi buku telepon digital dengan GUI Tkinter, memakai 3 struktur data:
- **AVL Tree** -> menyimpan kontak terurut nama, insert/search/delete O(log n)
- **Hash Table** -> mencari kontak lewat nomor telepon secara instan, O(1)
- **Trie** -> fitur autocomplete/prefix search nama, O(m) (m = panjang teks yang diketik)

## Struktur Folder

```
contact_manager/
├── main.py                     # Titik masuk aplikasi + GUI Tkinter
├── models/
│   └── contact.py               # Cetakan data satu kontak (nama, nomor, email)
├── structures/
│   ├── avl_tree.py               # Implementasi AVL Tree
│   ├── hash_table.py             # Implementasi Hash Table
│   └── trie.py                   # Implementasi Trie
├── services/
│   └── contact_manager.py       # "Otak" aplikasi, menggabungkan 3 struktur data
├── utils/
│   └── validators.py            # Validasi nomor telepon, nama, email
└── data/                        # Folder kosong, tempat menyimpan file CSV ekspor/impor
```

## Cara Menjalankan
```bash
cd contact_manager
python main.py
```

## Fitur di GUI

1. **Tambah Kontak** - isi form lalu klik "Tambah Kontak"
2. **Cari Nama** - pencarian cepat lewat AVL Tree
3. **Cari Nomor** - pencarian instan lewat Hash Table
4. **Klik baris di tabel** - form otomatis terisi, siap untuk Update/Hapus
5. **Ekspor ke CSV** - simpan semua kontak ke file .csv
6. **Impor dari CSV** - baca file .csv dan tambahkan sebagai kontak baru

## Kompleksitas (Big-O)

| Operasi                | Struktur Data | Kompleksitas |
|-------------------------|---------------|--------------|
| Insert/Search/Delete    | AVL Tree      | O(log n)     |
| Lookup nomor telepon    | Hash Table    | O(1)         |
| Prefix search (autocomplete) | Trie    | O(m)         |
