"""
FILE INI: TAMPILAN APLIKASI (GUI) pakai Tkinter.

Kalau file-file sebelumnya adalah "mesin" di balik layar (struktur data),
file ini adalah "dashboard mobil"-nya: tombol, kotak isian, dan tabel yang
bisa dipakai user awam tanpa perlu tahu ada AVL Tree/Hash Table/Trie di baliknya.

Fitur pencarian di sini pakai PREFIX SEARCH (pencarian awalan):
- Ketik "wahyu" di kotak cari nama -> langsung muncul semua "Wahyu ..." (live, sambil ngetik)
- Ketik "0815" di kotak cari nomor -> langsung muncul semua nomor yang diawali "0815"

Cara jalankan: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from services.contact_manager import ContactManager

# ---------------------------------------------------------------------------
# PALET WARNA - biar tampilannya konsisten dan enak dilihat 
# ---------------------------------------------------------------------------
WARNA_HEADER = "#0f6d5c"        # teal tua untuk header
WARNA_HEADER_TEKS = "#ffffff"
WARNA_AKSEN = "#0f6d5c"         # teal untuk tombol utama & border aktif
WARNA_LATAR = "#f4f6f7"         # abu-abu sangat muda untuk latar belakang
WARNA_KARTU = "#ffffff"         # putih untuk "kartu" form/panel
WARNA_TEKS_UTAMA = "#1f2d2b"
WARNA_TEKS_MUTED = "#6b7a77"
WARNA_SUKSES = "#0f8a5f"
WARNA_GAGAL = "#c0392b"
WARNA_ZEBRA_GANJIL = "#ffffff"
WARNA_ZEBRA_GENAP = "#eef5f3"
WARNA_SELEKSI = "#cfeee3"

FONT_UTAMA = ("Segoe UI", 10)
FONT_JUDUL = ("Segoe UI", 15, "bold")
FONT_SUBJUDUL = ("Segoe UI", 9)
FONT_LABEL_TEBAL = ("Segoe UI", 10, "bold")


class EntryDenganPlaceholder(ttk.Entry):
    """
    Kotak isian jadi user bisa isi data kontak
    """

    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_aktif = False
        self._tampilkan_placeholder()
        self.bind("<FocusIn>", self._saat_fokus_masuk)
        self.bind("<FocusOut>", self._saat_fokus_keluar)

    def _tampilkan_placeholder(self):
        self.insert(0, self.placeholder)
        self.configure(foreground="#9aa5a3")
        self.placeholder_aktif = True

    def _saat_fokus_masuk(self, event):
        if self.placeholder_aktif:
            self.delete(0, tk.END)
            self.configure(foreground=WARNA_TEKS_UTAMA)
            self.placeholder_aktif = False

    def _saat_fokus_keluar(self, event):
        if not self.get():
            self._tampilkan_placeholder()

    def get_nilai_asli(self):
        """Ambil isi kotak, tapi kembalikan string kosong kalau isinya cuma placeholder."""
        return "" if self.placeholder_aktif else self.get().strip()

    def kosongkan(self):
        self.delete(0, tk.END)
        self._tampilkan_placeholder()

    def isi_dengan(self, teks):
        self.delete(0, tk.END)
        self.configure(foreground=WARNA_TEKS_UTAMA)
        self.insert(0, teks)
        self.placeholder_aktif = False


class AplikasiKontak(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Kontak Telepon - Kelompok 5")
        self.geometry("1000x640")
        self.minsize(900, 560)
        self.configure(bg=WARNA_LATAR)

        self.manager = ContactManager()
        self.nomor_terpilih = None  

        self._buat_gaya_tampilan()
        self._buat_header()

        
        container = tk.Frame(self, bg=WARNA_LATAR)
        container.pack(fill="both", expand=True, padx=16, pady=12)
        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self._buat_panel_form(container)
        self._buat_panel_kanan(container)
        self._buat_status_bar()

        self._refresh_tabel()

    def _buat_gaya_tampilan(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", font=FONT_UTAMA, background=WARNA_LATAR)
        style.configure("Kartu.TLabelframe", background=WARNA_KARTU, borderwidth=1, relief="solid")
        style.configure("Kartu.TLabelframe.Label", background=WARNA_KARTU, font=FONT_LABEL_TEBAL,
                         foreground=WARNA_AKSEN)
        style.configure("Kartu.TFrame", background=WARNA_KARTU)

        style.configure("TButton", padding=8, font=FONT_UTAMA)
        style.map("TButton", background=[("active", "#e6f2ef")])

        style.configure("Utama.TButton", background=WARNA_AKSEN, foreground="white", padding=8)
        style.map("Utama.TButton",
                  background=[("active", "#0c5a4c"), ("disabled", "#a9c9c2")])

        style.configure("Bahaya.TButton", background="#fdecea", foreground=WARNA_GAGAL, padding=8)
        style.map("Bahaya.TButton", background=[("active", "#f6cfc9")])

        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                         background="#e3efec", foreground=WARNA_TEKS_UTAMA)
        style.configure("Treeview", rowheight=28, font=FONT_UTAMA,
                         background=WARNA_KARTU, fieldbackground=WARNA_KARTU)
        style.map("Treeview", background=[("selected", WARNA_SELEKSI)],
                  foreground=[("selected", WARNA_TEKS_UTAMA)])

    def _buat_header(self):
        header = tk.Frame(self, bg=WARNA_HEADER, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header, text="📇  Sistem Manajemen Kontak Telepon",
            bg=WARNA_HEADER, fg=WARNA_HEADER_TEKS, font=FONT_JUDUL,
        ).pack(side="left", padx=20)

        tk.Label(
            header, text="Kelompok 5  •  AVL Tree · Hash Table · Trie",
            bg=WARNA_HEADER, fg="#d7ede7", font=FONT_SUBJUDUL,
        ).pack(side="left")

        self.label_jumlah_header = tk.Label(
            header, text="Total kontak: 0", bg=WARNA_HEADER, fg="#d7ede7", font=FONT_SUBJUDUL,
        )
        self.label_jumlah_header.pack(side="right", padx=20)

    def _buat_panel_form(self, parent):
        panel = ttk.LabelFrame(parent, text="  Form Kontak (Tambah / Edit)  ", style="Kartu.TLabelframe")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        isi = ttk.Frame(panel, style="Kartu.TFrame")
        isi.pack(fill="both", expand=True, padx=16, pady=16)

        ttk.Label(isi, text="Nama Lengkap", background=WARNA_KARTU, font=FONT_LABEL_TEBAL).pack(anchor="w")
        self.input_nama = EntryDenganPlaceholder(isi, placeholder="Contoh: Budi Santoso", width=32)
        self.input_nama.pack(fill="x", pady=(2, 2))
        self.input_nama.bind("<KeyRelease>", self._saat_ketik_nama)

        self.saran_nama_var = tk.StringVar()
        ttk.Label(isi, textvariable=self.saran_nama_var, background=WARNA_KARTU,
                  foreground=WARNA_SUKSES, font=("Segoe UI", 8), wraplength=260).pack(anchor="w", pady=(0, 10))

        ttk.Label(isi, text="Nomor HP", background=WARNA_KARTU, font=FONT_LABEL_TEBAL).pack(anchor="w")
        self.input_nomor = EntryDenganPlaceholder(isi, placeholder="Contoh: 081234567890", width=32)
        self.input_nomor.pack(fill="x", pady=(2, 10))

        ttk.Label(isi, text="Email (opsional)", background=WARNA_KARTU, font=FONT_LABEL_TEBAL).pack(anchor="w")
        self.input_email = EntryDenganPlaceholder(isi, placeholder="Contoh: budi@email.com", width=32)
        self.input_email.pack(fill="x", pady=(2, 16))

        ttk.Button(isi, text="➕  Tambah Kontak", style="Utama.TButton",
                   command=self._tambah_kontak).pack(fill="x", pady=3)
        ttk.Button(isi, text="✎  Update Kontak Terpilih",
                   command=self._update_kontak).pack(fill="x", pady=3)
        ttk.Button(isi, text="🗑  Hapus Kontak Terpilih", style="Bahaya.TButton",
                   command=self._hapus_kontak).pack(fill="x", pady=3)
        ttk.Button(isi, text="↺  Bersihkan Form",
                   command=self._bersihkan_form).pack(fill="x", pady=3)

        ttk.Separator(isi).pack(fill="x", pady=14)

        ttk.Label(isi, text="Data (Import / Export)", background=WARNA_KARTU,
                  font=FONT_LABEL_TEBAL).pack(anchor="w", pady=(0, 6))
        ttk.Button(isi, text="⇩  Ekspor ke CSV", command=self._ekspor_csv).pack(fill="x", pady=3)
        ttk.Button(isi, text="⇧  Impor dari CSV", command=self._impor_csv).pack(fill="x", pady=3)

        # Label kecil penanda kontak yang sedang dipilih untuk edit
        self.label_status_pilihan = ttk.Label(
            isi, text="Belum ada kontak dipilih.", background=WARNA_KARTU,
            foreground=WARNA_TEKS_MUTED, font=("Segoe UI", 8, "italic"), wraplength=260,
        )
        self.label_status_pilihan.pack(anchor="w", pady=(12, 0))

    def _saat_ketik_nama(self, event):
        """Setiap kali user mengetik di kotak nama, tampilkan saran dari Trie (autocomplete)."""
        prefix = self.input_nama.get_nilai_asli()
        if not prefix:
            self.saran_nama_var.set("")
            return
        saran = self.manager.autocomplete_nama(prefix)
        if saran:
            self.saran_nama_var.set("💡 Mirip dengan: " + ", ".join(s.title() for s in saran[:5]))
        else:
            self.saran_nama_var.set("Nama baru, belum ada yang mirip.")


    def _buat_panel_kanan(self, parent):
        kanan = ttk.Frame(parent, style="Kartu.TFrame")
        kanan.grid(row=0, column=1, sticky="nsew")
        kanan.rowconfigure(1, weight=1)
        kanan.columnconfigure(0, weight=1)

        self._buat_area_pencarian(kanan)
        self._buat_tabel_kontak(kanan)

    def _buat_area_pencarian(self, parent):
        panel = ttk.LabelFrame(parent, text="  Pencarian (langsung tampil sambil mengetik)  ",
                                style="Kartu.TLabelframe")
        panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        isi = ttk.Frame(panel, style="Kartu.TFrame")
        isi.pack(fill="x", padx=16, pady=12)

        ttk.Label(isi, text="🔎 Cari Nama (awalan)", background=WARNA_KARTU,
                  font=FONT_LABEL_TEBAL).grid(row=0, column=0, sticky="w")
        self.cari_nama_entry = EntryDenganPlaceholder(isi, placeholder="Ketik: wahyu ...", width=28)
        self.cari_nama_entry.grid(row=1, column=0, sticky="w", padx=(0, 20))
        self.cari_nama_entry.bind("<KeyRelease>", self._saat_ketik_cari)

        ttk.Label(isi, text="🔎 Cari Nomor HP (awalan)", background=WARNA_KARTU,
                  font=FONT_LABEL_TEBAL).grid(row=0, column=1, sticky="w")
        self.cari_nomor_entry = EntryDenganPlaceholder(isi, placeholder="Ketik: 0815 ...", width=28)
        self.cari_nomor_entry.grid(row=1, column=1, sticky="w", padx=(0, 20))
        self.cari_nomor_entry.bind("<KeyRelease>", self._saat_ketik_cari)

        ttk.Button(isi, text="Tampilkan Semua", command=self._reset_pencarian).grid(
            row=1, column=2, sticky="e", padx=(0, 0))

        isi.columnconfigure(2, weight=1)

    def _saat_ketik_cari(self, event):
        """
        LIVE SEARCH: dipanggil otomatis tiap kali user mengetik di salah satu
        kotak pencarian. Tidak perlu klik tombol apa pun.
        """
        kata_nama = self.cari_nama_entry.get_nilai_asli()
        kata_nomor = self.cari_nomor_entry.get_nilai_asli()

        if not kata_nama and not kata_nomor:
            self._refresh_tabel()
            return

        hasil_nama = self.manager.cari_nama_awalan(kata_nama) if kata_nama else None
        hasil_nomor = self.manager.cari_nomor_awalan(kata_nomor) if kata_nomor else None

        if hasil_nama is not None and hasil_nomor is not None:
            nomor_di_hasil_nomor = {k.nomor for k in hasil_nomor}
            hasil = [k for k in hasil_nama if k.nomor in nomor_di_hasil_nomor]
        else:
            hasil = hasil_nama if hasil_nama is not None else hasil_nomor

        self._tampilkan_daftar(hasil)
        self._update_info_jumlah(f"Ditemukan {len(hasil)} kontak cocok.")

    def _reset_pencarian(self):
        self.cari_nama_entry.kosongkan()
        self.cari_nomor_entry.kosongkan()
        self._refresh_tabel()


    def _buat_tabel_kontak(self, parent):
        panel = ttk.LabelFrame(parent, text="  Daftar Kontak (terurut A-Z)  ", style="Kartu.TLabelframe")
        panel.grid(row=1, column=0, sticky="nsew")
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)

        frame = ttk.Frame(panel, style="Kartu.TFrame")
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        kolom = ("nama", "nomor", "email")
        self.tabel = ttk.Treeview(frame, columns=kolom, show="headings", selectmode="browse")
        self.tabel.heading("nama", text="Nama")
        self.tabel.heading("nomor", text="Nomor HP")
        self.tabel.heading("email", text="Email")
        self.tabel.column("nama", width=260)
        self.tabel.column("nomor", width=170)
        self.tabel.column("email", width=260)

        self.tabel.tag_configure("ganjil", background=WARNA_ZEBRA_GANJIL)
        self.tabel.tag_configure("genap", background=WARNA_ZEBRA_GENAP)

        self.tabel.grid(row=0, column=0, sticky="nsew")
        self.tabel.bind("<<TreeviewSelect>>", self._saat_pilih_baris)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _tampilkan_daftar(self, daftar_kontak):
        """Menggambar ulang isi tabel sesuai daftar kontak yang diberikan."""
        for baris in self.tabel.get_children():
            self.tabel.delete(baris)
        for i, kontak in enumerate(daftar_kontak):
            tag = "genap" if i % 2 == 0 else "ganjil"
            self.tabel.insert("", "end", values=(kontak.nama, kontak.nomor, kontak.email), tags=(tag,))

    def _refresh_tabel(self):
        """Menampilkan semua kontak, terurut A-Z (langsung dari AVL Tree)."""
        semua = self.manager.semua_kontak_terurut()
        self._tampilkan_daftar(semua)
        self._update_info_jumlah("Menampilkan semua kontak.")

    def _saat_pilih_baris(self, event):
        """Waktu user klik satu baris di tabel, form otomatis keisi datanya (siap update/hapus)."""
        item_terpilih = self.tabel.selection()
        if not item_terpilih:
            return
        nilai = self.tabel.item(item_terpilih[0], "values")
        nama, nomor, email = nilai
        self.input_nama.isi_dengan(nama)
        self.input_nomor.isi_dengan(nomor)
        self.input_email.isi_dengan(email)
        self.saran_nama_var.set("")
        self.nomor_terpilih = nomor
        self.label_status_pilihan.config(text=f"✔ Sedang mengedit: {nama}", foreground=WARNA_SUKSES)

    # ---------------------------------------------------------------
    # AKSI UTAMA: TAMBAH / UPDATE / HAPUS / EKSPOR / IMPOR
    # ---------------------------------------------------------------

    def _tambah_kontak(self):
        nama = self.input_nama.get_nilai_asli()
        nomor = self.input_nomor.get_nilai_asli()
        email = self.input_email.get_nilai_asli()

        berhasil, pesan = self.manager.tambah_kontak(nama, nomor, email)
        self._tampilkan_pesan(berhasil, pesan)
        if berhasil:
            self._bersihkan_form()
            self._refresh_tabel()

    def _update_kontak(self):
        if not self.nomor_terpilih:
            messagebox.showwarning("Perhatian", "Pilih dulu kontak dari tabel yang mau diupdate.")
            return

        nama_baru = self.input_nama.get_nilai_asli()
        nomor_baru = self.input_nomor.get_nilai_asli()
        email_baru = self.input_email.get_nilai_asli()

        berhasil, pesan = self.manager.update_kontak(self.nomor_terpilih, nama_baru, nomor_baru, email_baru)
        self._tampilkan_pesan(berhasil, pesan)
        if berhasil:
            self._bersihkan_form()
            self._refresh_tabel()

    def _hapus_kontak(self):
        if not self.nomor_terpilih:
            messagebox.showwarning("Perhatian", "Pilih dulu kontak dari tabel yang mau dihapus.")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin mau hapus kontak ini?")
        if not konfirmasi:
            return

        berhasil, pesan = self.manager.hapus_kontak(self.nomor_terpilih)
        self._tampilkan_pesan(berhasil, pesan)
        if berhasil:
            self._bersihkan_form()
            self._refresh_tabel()

    def _ekspor_csv(self):
        path_file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Simpan kontak sebagai...",
        )
        if not path_file:
            return
        berhasil, pesan = self.manager.ekspor_csv(path_file)
        self._tampilkan_pesan(berhasil, pesan)

    def _impor_csv(self):
        path_file = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Pilih file CSV kontak",
        )
        if not path_file:
            return
        berhasil, pesan = self.manager.impor_csv(path_file)
        self._tampilkan_pesan(berhasil, pesan)
        if berhasil:
            self._refresh_tabel()


    def _buat_status_bar(self):
        bar = tk.Frame(self, bg="#e3efec", height=30)
        bar.pack(fill="x", side="bottom")
        self.label_info = tk.Label(bar, text="Siap digunakan.", bg="#e3efec",
                                    fg=WARNA_TEKS_MUTED, font=("Segoe UI", 9), anchor="w")
        self.label_info.pack(side="left", padx=14, pady=4)

    def _update_info_jumlah(self, teks_tambahan=""):
        total = len(self.manager.semua_kontak_terurut())
        self.label_jumlah_header.config(text=f"Total kontak: {total}")
        if teks_tambahan:
            self.label_info.config(text=teks_tambahan, fg=WARNA_TEKS_MUTED)

    def _bersihkan_form(self):
        self.input_nama.kosongkan()
        self.input_nomor.kosongkan()
        self.input_email.kosongkan()
        self.saran_nama_var.set("")
        self.nomor_terpilih = None
        self.label_status_pilihan.config(text="Belum ada kontak dipilih.", foreground=WARNA_TEKS_MUTED)

    def _tampilkan_pesan(self, berhasil: bool, pesan: str):
        """Menampilkan pesan sukses/gagal di status bar, dan popup kalau gagal."""
        self.label_info.config(text=pesan, fg=WARNA_SUKSES if berhasil else WARNA_GAGAL)
        self._update_info_jumlah()
        if not berhasil:
            messagebox.showerror("Gagal", pesan)


if __name__ == "__main__":
    app = AplikasiKontak()
    app.mainloop()
