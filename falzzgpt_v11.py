# ==================================================
# FALZZGPT v11.0 - VERSI FIX ERROR + ADA DEVELOPER
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
# FOLDER OTOMATIS TANPA ERROR
# --------------------------
FOLDER = {
    "utama":        "./data/",
    "data_aman":    "./data/DATA_AMAN/",
    "proyek":       "./data/PROYEK/",
    "laporan":      "./data/LAPORAN/",
    "log":          "./data/LOG/",
    "pengaturan":   "./data/PENGATURAN/",
    "cadangan":     "./data/CADANGAN/"
}

def buat_semua_folder():
    for jalur in FOLDER.values():
        os.makedirs(jalur, exist_ok=True)

buat_semua_folder()

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

VERSI = "11.0"
KEY_DEVELOPER = "FALLSTORE01"
BIAYA_DAFTAR_ADMIN = 50000

DAFTAR_PAKET = {
    "PERCOBAAN": {"harga": 0, "durasi": 7, "nama": "Paket Percobaan (7 Hari)"},
    "BULANAN": {"harga": 15000, "durasi": 30, "nama": "Paket Bulanan"},
    "TAHUNAN": {"harga": 35000, "durasi": 365, "nama": "Paket Tahunan"},
    "PERMANEN": {"harga": 50000, "durasi": 99999, "nama": "Paket Permanen ✅"}
}

# ✅ SUDAH ADA OPSI DEVELOPER
JENIS_AKUN = ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1", "DEVELOPER"]

KUNCI_SIMETRIS = Fernet.generate_key()
cipher_simetris = Fernet(KUNCI_SIMETRIS)

# --------------------------
# FUNGSI MUAT & SIMPAN DATA
# --------------------------
def muat_akun():
    if os.path.exists(FILE["akun"]):
        try:
            with open(FILE["akun"], "rb") as f:
                return json.loads(cipher_simetris.decrypt(f.read()))
        except:
            return []
    return []

def simpan_akun(daftar):
    buat_semua_folder()
    with open(FILE["akun"], "wb") as f:
        f.write(cipher_simetris.encrypt(json.dumps(daftar).encode("utf-8")))

# --------------------------
# TAMPILAN UTAMA
# --------------------------
st.markdown("""
<style>
* {font-family: 'Inter', sans-serif; margin:0; padding:0; box-sizing:border-box;}
body {background: linear-gradient(145deg, #EEF2FF, #E0E7FF);}
.card {background: #fff; border-radius: 20px; padding: 28px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(22,93,255,0.12);}
h1 {color: #165DFF; text-align: center;}
</style>
""", unsafe_allow_html=True)

if "login" not in st.session_state:
    st.session_state.login = False
if "data_akun" not in st.session_state:
    st.session_state.data_akun = None

if not st.session_state.login:
    st.markdown("<div class='card'><h1>🛡️ FALZZGPT v11</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Daftar Akun", "🔑 Masuk Akun"])

    with tab1:
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        email = st.text_input("Email")
        jenis = st.selectbox("Daftar Sebagai", JENIS_AKUN)
        paket = st.selectbox("Pilih Paket Berlangganan", list(DAFTAR_PAKET.keys()), format_func=lambda x: DAFTAR_PAKET[x]["nama"])

        kunci_dev = ""
        bisa_daftar = True
        if jenis == "DEVELOPER":
            kunci_dev = st.text_input("Masukkan Kunci Developer", type="password", help="Kunci: FALLSTORE01")
            if kunci_dev != KEY_DEVELOPER:
                st.warning("⚠️ Masukkan kunci yang benar!")
                bisa_daftar = False
        else:
            if jenis != "PENGGUNA":
                st.info(f"ℹ️ Biaya jaminan: Rp{BIAYA_DAFTAR_ADMIN:,}")

        if st.button("Kirim Pendaftaran", type="primary", use_container_width=True, disabled=not bisa_daftar):
            if nama and hp and email:
                if jenis == "DEVELOPER":
                    status = "Aktif"
                    saldo = 9999999
                else:
                    status = "Belum Diverifikasi"
                    saldo = BIAYA_DAFTAR_ADMIN if jenis != "PENGGUNA" else 0

                akun_baru = {
                    "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                    "nama": nama,
                    "hp": hp,
                    "email": email,
                    "jenis": jenis,
                    "paket": paket,
                    "status": status,
                    "saldo": saldo,
                    "tgl_aktif": (datetime.now() + timedelta(days=DAFTAR_PAKET[paket]["durasi"])).isoformat(),
                    "dibuat": datetime.now().isoformat()
                }

                daftar = muat_akun()
                daftar.append(akun_baru)
                simpan_akun(daftar)

                if jenis == "DEVELOPER":
                    st.success("✅ BERHASIL! Akun Developer langsung AKTIF.")
                else:
                    st.success("✅ Pendaftaran terkirim, tunggu verifikasi.")
            else:
                st.warning("⚠️ Lengkapi semua data!")

    with tab2:
        id_masuk = st.text_input("ID Akun / Nomor HP")
        kunci_masuk = st.text_input("Kunci Khusus (Developer saja)", type="password", placeholder="Kosongkan jika bukan Developer")

        if st.button("Masuk Sekarang", type="primary", use_container_width=True):
            daftar = muat_akun()
            akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)

            if akun:
                if akun["jenis"] == "DEVELOPER" and kunci_masuk != KEY_DEVELOPER:
                    st.error("❌ Kunci Developer salah!")
                elif akun["status"] != "Aktif":
                    st.warning("⚠️ Akun belum aktif!")
                else:
                    st.session_state.login = True
                    st.session_state.data_akun = akun
                    st.rerun()
            else:
                st.error("❌ Akun tidak ditemukan!")

else:
    akun = st.session_state.data_akun
    menu = ["👤 PROFIL", "💳 BERLANGGANAN", "🤖 AI ASISTEN", "🚪 KELUAR"]
    if akun["jenis"] in ["ADMIN_1", "DEVELOPER"]:
        menu.insert(2, "✅ VERIFIKASI AKUN")

    menu_pilih = st.sidebar.selectbox("📋 MENU UTAMA", menu)
    st.sidebar.info(f"""
    📊 DATA AKUN
    • Nama: {akun['nama']}
    • Jenis: {akun['jenis']}
    • Status: {akun['status']}
    • Saldo: Rp{akun['saldo']:,}
    """)

    if menu_pilih == "🚪 KELUAR":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()
    elif menu_pilih == "✅ VERIFIKASI AKUN":
        st.subheader("✅ Verifikasi Akun Baru")
        daftar = muat_akun()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"ID: {a['id']} | Nama: {a['nama']} | Jenis: {a['jenis']}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=a["id"]):
                    a["status"] = "Aktif"
                    simpan_akun(daftar)
                    st.success("Akun diaktifkan!")
                    st.rerun()
        else:
            st.info("Tidak ada akun yang menunggu")
    elif menu_pilih == "🤖 AI ASISTEN":
        st.subheader("🤖 AI Asisten")
        pesan = st.text_area("Tanya apa saja:")
        if st.button("Kirim"):
            st.success("✅ Pesan diproses!")
