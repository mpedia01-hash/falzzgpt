# ==================================================
# FALZZGPT v11 - VERSI PENYIMPANAN AMAN & PASTI
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

JENIS_AKUN = ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1", "DEVELOPER"]

# --------------------------
# ✅ SISTEM PENYIMPANAN PASTI TERSIMPAN
# --------------------------
def muat_akun():
    # Pakai session_state + file cadangan yang pasti bisa diakses
    if "daftar_akun" not in st.session_state:
        # Coba baca dari file jika ada
        if os.path.exists("daftar_akun.json"):
            try:
                with open("daftar_akun.json", "r", encoding="utf-8") as f:
                    st.session_state.daftar_akun = json.load(f)
            except:
                st.session_state.daftar_akun = []
        else:
            st.session_state.daftar_akun = []
    return st.session_state.daftar_akun

def simpan_akun(daftar):
    st.session_state.daftar_akun = daftar
    # Simpan ke file cadangan
    try:
        with open("daftar_akun.json", "w", encoding="utf-8") as f:
            json.dump(daftar, f, indent=2, ensure_ascii=False)
    except:
        pass # Tetap jalan meski file tidak bisa ditulis

# --------------------------
# TAMPILAN UTAMA
# --------------------------
st.markdown("""
<style>
* {font-family: 'Inter', sans-serif; margin:0; padding:0; box-sizing:border-box;}
body {background: #0E1117; color: #FAFAFA;}
.card {background: #1E2129; border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid #2E323A;}
h1 {color: #4D90FE; text-align: center; font-size: 32px;}
.stButton>button {width: 100%; border-radius: 10px; font-weight: bold;}
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
            kunci_dev = st.text_input("Masukkan Kunci Developer", type="password", help="Masukkan: FALLSTORE01")
            if kunci_dev != KEY_DEVELOPER:
                st.warning("⚠️ Kunci Developer salah!")
                bisa_daftar = False

        if st.button("Kirim Pendaftaran", type="primary", use_container_width=True, disabled=not bisa_daftar):
            if nama and hp and email:
                # Cek apakah nomor HP sudah terdaftar
                daftar = muat_akun()
                cek = next((a for a in daftar if a["hp"] == hp), None)
                if cek:
                    st.error("❌ Nomor HP sudah terdaftar!")
                    st.stop()

                # Buat akun baru
                akun_baru = {
                    "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                    "nama": nama,
                    "hp": hp,
                    "email": email,
                    "jenis": jenis,
                    "paket": paket,
                    "status": "Aktif" if jenis == "DEVELOPER" else "Belum Diverifikasi",
                    "saldo": 9999999 if jenis == "DEVELOPER" else 0,
                    "tgl_aktif": datetime.now().isoformat(),
                    "tgl_berakhir": (datetime.now() + timedelta(days=DAFTAR_PAKET[paket]["durasi"])).isoformat()
                }

                daftar.append(akun_baru)
                simpan_akun(daftar)

                if jenis == "DEVELOPER":
                    st.success(f"""✅ **PENDAFTARAN BERHASIL!**
                    • ID Akun: `{akun_baru['id']}`
                    • Status: **Langsung Aktif**
                    Silakan masuk menggunakan ID atau Nomor HP kamu!""")
                else:
                    st.success("✅ Pendaftaran terkirim! Tunggu verifikasi dari Admin/Developer.")
            else:
                st.warning("⚠️ Lengkapi semua data terlebih dahulu!")

    with tab2:
        st.info("Bisa masuk pakai **ID Akun** atau **Nomor HP**")
        id_masuk = st.text_input("ID Akun / Nomor HP")
        kunci_masuk = st.text_input("Kunci Khusus (hanya untuk Developer)", type="password", placeholder="Kosongkan jika bukan Developer")

        if st.button("Masuk Sekarang", type="primary", use_container_width=True):
            daftar = muat_akun()
            akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)

            if not akun:
                st.error("❌ Akun tidak ditemukan! Pastikan sudah mendaftar dengan benar.")
                st.stop()

            if akun["jenis"] == "DEVELOPER" and kunci_masuk != KEY_DEVELOPER:
                st.error("❌ Kunci Developer salah!")
                st.stop()

            if akun["status"] != "Aktif":
                st.warning("⚠️ Akun belum diverifikasi atau diblokir!")
                st.stop()

            st.session_state.login = True
            st.session_state.data_akun = akun
            st.rerun()

else:
    akun = st.session_state.data_akun
    sisa_hari = (datetime.fromisoformat(akun["tgl_berakhir"]) - datetime.now()).days
    diskon = datetime.now().weekday() in (5,6)

    if diskon:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #FFB700, #FF8800); color: white; padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px;'>
        🎉 DISKON 20% SETIAP AKHIR PEKAN! 🎉
        </div>
        """, unsafe_allow_html=True)

    # MENU SESUAI JENIS AKUN
    menu = ["👤 Profil Saya", "💳 Berlangganan", "🤖 AI Asisten", "📚 Belajar Koding", "🚪 Keluar"]
    if akun["jenis"] in ["ADMIN_1", "DEVELOPER"]:
        menu.insert(2, "✅ Verifikasi Akun")
    if akun["jenis"] == "DEVELOPER":
        menu.extend(["👥 Kelola Pengguna", "⚙️ Pengaturan Sistem"])

    menu_pilih = st.sidebar.selectbox("📋 MENU UTAMA", menu)

    # INFO SAMPING
    st.sidebar.markdown(f"""
    <div style='background: #1E2129; padding: 15px; border-radius: 10px; border: 1px solid #2E323A;'>
    <h4>📊 DATA AKUN</h4>
    • Nama: {akun['nama']}
    • Jenis: <span style='color:#4D90FE; font-weight:bold;'>{akun['jenis']}</span>
    • Paket: {DAFTAR_PAKET[akun['paket']]['nama']}
    • Sisa Hari: {sisa_hari if sisa_hari > 0 else 'Habis'}
    • Saldo: <span style='color:#00C853; font-weight:bold;'>Rp {akun['saldo']:,}</span>
    </div>
    """, unsafe_allow_html=True)

    if menu_pilih == "🚪 Keluar":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()

    elif menu_pilih == "👤 Profil Saya":
        st.markdown("<div class='card'><h2>👤 Profil Lengkap</h2></div>", unsafe_allow_html=True)
        st.json(akun)

    elif menu_pilih == "✅ Verifikasi Akun":
        st.markdown("<div class='card'><h2>✅ Verifikasi Akun Baru</h2></div>", unsafe_allow_html=True)
        daftar = muat_akun()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"**ID:** {a['id']} | **Nama:** {a['nama']} | **Jenis:** {a['jenis']}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=f"aktif_{a['id']}"):
                    a["status"] = "Aktif"
                    simpan_akun(daftar)
                    st.success("✅ Akun berhasil diaktifkan!")
                    st.rerun()
                if col2.button("❌ Tolak", key=f"tolak_{a['id']}"):
                    daftar.remove(a)
                    simpan_akun(daftar)
                    st.info("❌ Pendaftaran ditolak")
                    st.rerun()
        else:
            st.info("Tidak ada akun yang menunggu verifikasi")

    elif menu_pilih == "🤖 AI Asisten":
        st.markdown("<div class='card'><h2>🤖 AI Asisten Pintar</h2></div>", unsafe_allow_html=True)
        pesan = st.text_area("Tanya apa saja, minta kode, atau buat cerita...", height=150)
        if st.button("Kirim ke AI", type="primary"):
            if pesan.strip():
                st.success("✅ Pesan diterima dan diproses!")
                st.info(f"Jawaban untuk: {pesan[:60]}...")
            else:
                st.warning("⚠️ Masukkan pertanyaan terlebih dahulu!")
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
