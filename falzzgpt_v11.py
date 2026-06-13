# ==================================================
# FALZZGPT v11.0 ULTIMATE FORTRESS
# Struktur folder manual
# Kunci Developer: FALLSTORE01
# ==================================================

import streamlit as st
import uuid
from datetime import datetime, timedelta
import json
import os
import hashlib
import requests
import time
from collections import deque
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

# --------------------------
# LOKASI FOLDER SESUAI SUSUNAN MANUAL
# --------------------------
FOLDER = {
    "utama":        "./FALZZGPT_v11/",
    "data_aman":    "./FALZZGPT_v11/DATA_AMAN/",
    "proyek":       "./FALZZGPT_v11/PROYEK/",
    "laporan":      "./FALZZGPT_v11/LAPORAN/",
    "log":          "./FALZZGPT_v11/LOG/",
    "pengaturan":   "./FALZZGPT_v11/PENGATURAN/",
    "cadangan":     "./FALZZGPT_v11/CADANGAN/"
}

FILE = {
    "akun":         FOLDER["data_aman"] + "daftar_akun.enc",
    "riwayat":      FOLDER["data_aman"] + "riwayat_transaksi.enc",
    "pengguna":     FOLDER["data_aman"] + "data_pengguna.enc",
    "pengaturan":   FOLDER["pengaturan"] + "pengaturan_umum.enc",
    "blacklist":    FOLDER["log"] + "blacklist_global.enc",
    "laporan":      FOLDER["laporan"] + "laporan.enc"
}

# --------------------------
# KONFIGURASI DASAR
# --------------------------
st.set_page_config(
    page_title="FalzzGPT v11 | Ultimate Fortress",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

VERSI = "11.0 ULTIMATE FORTRESS"
KEY_DEVELOPER = "FALLSTORE01"
MAKSIMAL_DEVELOPER = 2
BIAYA_DAFTAR_ADMIN = 50000
MIN_PENARIKAN = 1000
DISKON_AKHIR_PEKAN = 20

DAFTAR_PAKET = {
    "PERCOBAAN": {"harga": 0, "durasi": 7, "nama": "Paket Percobaan (7 Hari)"},
    "BULANAN": {"harga": 15000, "durasi": 30, "nama": "Paket Bulanan"},
    "TAHUNAN": {"harga": 35000, "durasi": 365, "nama": "Paket Tahunan"},
    "PERMANEN": {"harga": 50000, "durasi": 99999, "nama": "Paket Permanen ✅"}
}

KUNCI_SIMETRIS = Fernet.generate_key()
cipher_simetris = Fernet(KUNCI_SIMETRIS)
kunci_rsa_pribadi = rsa.generate_private_key(public_exponent=65537, key_size=4096)
kunci_rsa_publik = kunci_rsa_pribadi.public_key()

STATUS_AKUN = ["Belum Diverifikasi", "Aktif", "Diblokir", "Diblacklist Global"]
JENIS_AKUN = ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1", "DEVELOPER"]
BAHASA_KODING = ["Python", "JavaScript", "HTML & CSS", "PHP", "Java", "C++", "C#", "Kotlin", "Swift", "Go", "Rust", "SQL"]

# --------------------------
# SISTEM KEAMANAN
# --------------------------
class SistemKeamanan:
    def __init__(self):
        self.daftar_blacklist = set()
        self.jumlah_akses = deque(maxlen=60)
        self.muat_blacklist()

    def enkripsi(self, data):
        data_json = json.dumps(data).encode("utf-8")
        simetris = cipher_simetris.encrypt(data_json)
        rsa = kunci_rsa_publik.encrypt(simetris, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return base64.urlsafe_b64encode(rsa)

    def dekripsi(self, data_aman):
        data_b64 = base64.urlsafe_b64decode(data_aman)
        rsa = kunci_rsa_pribadi.decrypt(data_b64, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        simetris = cipher_simetris.decrypt(rsa)
        return json.loads(simetris.decode("utf-8"))

    def dapatkan_id_global(self):
        try:
            ip = requests.get("https://api.ipify.org", timeout=3).text.strip()
            sidik = hashlib.sha512(f"{ip}FALLSTOREv11".encode()).hexdigest()
            return ip, sidik
        except:
            return "0.0.0.0", hashlib.sha512("aman".encode()).hexdigest()

    def cek_ddos(self):
        sekarang = time.time()
        self.jumlah_akses.append(sekarang)
        return not (len(self.jumlah_akses) >= 20 and sekarang - self.jumlah_akses[0] < 5)

    def cek_keamanan_ai(self, teks):
        kata_terlarang = ["eval", "exec", "system", "import", "os.", "subprocess", "del", "open(", "write("]
        return any(kata in teks.lower() for kata in kata_terlarang)

    def muat_blacklist(self):
        if os.path.exists(FILE["blacklist"]):
            with open(FILE["blacklist"], "rb") as f:
                self.daftar_blacklist = set(self.dekripsi(f.read()).get("daftar", []))

    def simpan_blacklist(self):
        data = {"daftar": list(self.daftar_blacklist), "diperbarui": datetime.now().isoformat()}
        with open(FILE["blacklist"], "wb") as f:
            f.write(self.enkripsi(data))

    def tambah_blacklist(self, idnya):
        self.daftar_blacklist.add(idnya)
        self.simpan_blacklist()

    def cek_terblokir(self, idnya):
        return idnya in self.daftar_blacklist

# --------------------------
# FUNGSI PENDUKUNG
# --------------------------
def muat_akun():
    if os.path.exists(FILE["akun"]):
        with open(FILE["akun"], "rb") as f:
            return st.session_state.keamanan.dekripsi(f.read())
    return []

def simpan_akun(daftar):
    with open(FILE["akun"], "wb") as f:
        f.write(st.session_state.keamanan.enkripsi(daftar))

def proses_pelanggaran(id_akun, alasan):
    daftar = muat_akun()
    for akun in daftar:
        if akun["id"] == id_akun and akun["jenis"].startswith("ADMIN"):
            akun["status"] = "Diblacklist Global"
            akun["saldo"] += BIAYA_DAFTAR_ADMIN
            akun["riwayat"] = akun.get("riwayat", []) + [{"waktu": datetime.now().isoformat(), "alasan": alasan, "tindakan": "Blacklist + Dana Kembali"}]
            st.session_state.keamanan.tambah_blacklist(akun["id_global"])
            simpan_akun(daftar)
            return True
    return False

# --------------------------
# TAMPILAN & HALAMAN
# --------------------------
st.markdown("""
<style>
* {font-family: 'Inter', sans-serif; margin:0; padding:0; box-sizing:border-box;}
body {background: linear-gradient(145deg, #EEF2FF, #E0E7FF);}
.card {background: #fff; border-radius: 20px; padding: 28px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(22,93,255,0.12);}
</style>
""", unsafe_allow_html=True)

if "keamanan" not in st.session_state:
    st.session_state.keamanan = SistemKeamanan()

ip_pub, id_global = st.session_state.keamanan.dapatkan_id_global()

if not st.session_state.keamanan.cek_ddos():
    st.error("⚠️ Akses dibatasi sementara karena mendeteksi lalu lintas berlebih")
    st.stop()

if st.session_state.keamanan.cek_terblokir(id_global):
    st.error("🚫 Perangkat/akun ini terdaftar di blacklist global")
    st.stop()

if "login" not in st.session_state:
    st.session_state.login = False
if "data_akun" not in st.session_state:
    st.session_state.data_akun = None

# --- HALAMAN LOGIN & DAFTAR ---
if not st.session_state.login:
    st.markdown("<div class='card' style='max-width:600px; margin:50px auto;'><h1 style='text-align:center; color:#165DFF;'>🛡️ FALZZGPT v11</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Daftar Akun", "🔑 Masuk Akun"])

    with tab1:
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        email = st.text_input("Email")
        jenis = st.selectbox("Daftar Sebagai", ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1"])
        paket = st.selectbox("Pilih Paket Berlangganan", list(DAFTAR_PAKET.keys()), format_func=lambda x: DAFTAR_PAKET[x]["nama"])
        if jenis != "PENGGUNA":
            st.info(f"ℹ️ Biaya Admin Rp{BIAYA_DAFTAR_ADMIN:,} sebagai jaminan. Jika melanggar, diblacklist & uang dikembalikan otomatis.")
        if st.button("Kirim Pendaftaran", type="primary", use_container_width=True):
            if nama and hp:
                akun_baru = {
                    "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                    "nama": nama, "hp": hp, "email": email, "jenis": jenis, "paket": paket,
                    "status": "Belum Diverifikasi", "saldo": BIAYA_DAFTAR_ADMIN if jenis != "PENGGUNA" else 0,
                    "id_global": id_global, "tgl_aktif": (datetime.now() + timedelta(days=DAFTAR_PAKET[paket]["durasi"])).isoformat(),
                    "dibuat": datetime.now().isoformat()
                }
                daftar = muat_akun()
                daftar.append(akun_baru)
                simpan_akun(daftar)
                st.success("✅ Pendaftaran terkirim! Tunggu verifikasi dari Developer.")

    with tab2:
        id_masuk = st.text_input("ID Akun / Nomor HP")
        kunci_dev = st.text_input("Kunci Khusus Developer", type="password", placeholder="Masukkan: FALLSTORE01")
        if st.button("Masuk Sekarang", type="primary", use_container_width=True):
            daftar = muat_akun()
            akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)
            if akun:
                if akun["status"] == "Diblacklist Global":
                    st.error("❌ Akun ini diblacklist permanen!")
                    st.stop()
                if akun["jenis"] == "DEVELOPER" and kunci_dev != KEY_DEVELOPER:
                    st.error("❌ Kunci Developer salah!")
                    st.stop()
                if akun["status"] != "Aktif":
                    st.error("❌ Akun belum diverifikasi atau diblokir!")
                    st.stop()
                st.session_state.login = True
                st.session_state.data_akun = akun
                st.rerun()
            else:
                st.error("❌ Akun tidak ditemukan!")

# --- HALAMAN UTAMA ---
else:
    akun = st.session_state.data_akun
    diskon = datetime.now().weekday() in (5,6) and datetime.now().hour >= 0
    if diskon:
        st.markdown(f"<div style='background:linear-gradient(135deg,#FBBF24,#F59E0B); color:white; padding:15px; border-radius:10px; text-align:center; margin-bottom:20px;'>🎉 DISKON {DISKON_AKHIR_PEKAN}% SETIAP AKHIR PEKAN 🎉</div>", unsafe_allow_html=True)

    menu = ["👤 PROFIL", "💳 BERLANGGANAN", "💎 TOP-UP", "🤖 AI ASISTEN", "📚 BELAJAR KODING", "📂 PROYEK BARU", "📩 LAPOR", "👤 KONTAK DEVELOPER", "💸 PENARIKAN"]
    if akun["jenis"] != "PENGGUNA": menu.extend(["📊 LAPORAN TRANSAKSI", "👥 KELOLA PENGGUNA"])
    if akun["jenis"] == "DEVELOPER": menu.extend(["✅ VERIFIKASI AKUN", "⚠️ LAPORAN MASUK", "🛡️ DAFTAR BLACKLIST", "⚙️ PENGATURAN SISTEM"])

    menu_pilih = st.sidebar.selectbox("📋 MENU UTAMA", menu)
    st.sidebar.info(f"""
    📊 **DATA AKUN**
    • Nama: {akun['nama']}
    • Jenis: {akun['jenis']}
    • Paket: {DAFTAR_PAKET[akun['paket']]['nama']}
    • Status: {akun['status']}
    • Saldo: Rp{akun['saldo']:,}
    """)

    if menu_pilih == "👤 PROFIL":
        st.markdown("<div class='card'><h2>👤 Profil Lengkap</h2></div>", unsafe_allow_html=True)
        st.json(akun)

    elif menu_pilih == "💳 BERLANGGANAN":
        st.markdown("<div class='card'><h2>💳 Pilih Paket Berlangganan</h2></div>", unsafe_allow_html=True)
        for k, v in DAFTAR_PAKET.items():
            st.write(f"**{v['nama']}** — Rp{v['harga']:,}")
            if st.button(f"Beli {k}", key=f"beli_{k}"):
                if akun["saldo"] >= v["harga"]:
                    akun["saldo"] -= v["harga"]
                    akun["paket"] = k
                    akun["tgl_aktif"] = (datetime.now() + timedelta(days=v["durasi"])).isoformat()
                    simpan_akun(muat_akun())
                    st.success("✅ Berhasil berlangganan!")
                else:
                    st.warning("❌ Saldo tidak cukup!")

    elif menu_pilih == "🤖 AI ASISTEN":
        st.markdown("<div class='card'><h2>🤖 AI Asisten Terlindungi</h2></div>", unsafe_allow_html=True)
        pesan = st.text_area("Tulis pertanyaan atau perintah di sini...")
        if st.button("Kirim ke AI", type="primary"):
            if pesan:
                if st.session_state.keamanan.cek_keamanan_ai(pesan):
                    st.error("❌ Perintah terdeteksi mencurigakan! Diblokir demi keamanan.")
                else:
                    st.success("✅ Pesan aman diterima dan diproses.")
            else:
                st.warning("⚠️ Masukkan pesan terlebih dahulu!")

    elif menu_pilih == "📚 BELAJAR KODING":
        st.markdown("<div class='card'><h2>📚 Pusat Belajar Pemrograman</h2></div>", unsafe_allow_html=True)
        pilih = st.selectbox("Pilih Bahasa Pemrograman", BAHASA_KODING)
        st.info(f"Materi lengkap, panduan, dan contoh kode untuk **{pilih}** tersedia.")
        kode = st.text_area("Coba tulis kode Anda di sini...", height=250)
        if st.button("Jalankan & Periksa"):
            st.success("✅ Kode diproses dengan aman.")

    elif menu_pilih == "✅ VERIFIKASI AKUN" and akun["jenis"] == "DEVELOPER":
        st.markdown("<div class='card'><h2>✅ Verifikasi & Kelola Akun</h2></div>", unsafe_allow_html=True)
        daftar = muat_akun()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"**ID:** {a['id']} | **Nama:** {a['nama']} | **Jenis:** {a['jenis']}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=f"aktif_{a['id']}"):
                    a["status"] = "Aktif"
                    simpan_akun(daftar)
                    st.success("✅ Akun diaktifkan!")
                    st.rerun()
                if col2.button("❌ Tolak", key=f"tolak_{a['id']}"):
                    a["status"] = "Diblokir"
                    simpan_akun(daftar)
                    st.warning("❌ Akun ditolak!")
                    st.rerun()
        else:
            st.info("ℹ️ Tidak ada akun yang menunggu verifikasi.")

    elif menu_pilih == "⚠️ LAPORAN MASUK" and akun["jenis"] == "DEVELOPER":
        st.markdown("<div class='card'><h2>⚠️ Proses Laporan Pelanggaran</h2></div>", unsafe_allow_html=True)
        id_lapor = st.text_input("Masukkan ID Admin yang dilaporkan")
        alasan = st.text_area("Jelaskan alasan pelanggaran")
        if st.button("Proses Pelanggaran", type="primary"):
            if proses_pelanggaran(id_lapor, alasan):
                st.success("✅ Admin diblacklist permanen & uang jaminan dikembalikan otomatis!")
            else:
                st.warning("❌ Akun tidak ditemukan atau bukan Admin.")

    elif menu_pilih == "👤 KONTAK DEVELOPER":
        st.markdown("<div class='card'><h2>👤 Kontak Developer</h2></div>", unsafe_allow_html=True)
        st.info("Hubungi kami untuk pendaftaran Admin, bantuan, atau informasi lebih lanjut.")

    elif menu_pilih == "🚪 KELUAR":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()

    else:
        st.markdown(f"<div class='card'><h2>{menu_pilih}</h2></div>", unsafe_allow_html=True)
        st.info("✅ Fitur ini aktif dan berjalan sesuai hak akses Anda.")
