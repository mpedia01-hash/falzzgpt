# ==================================================
# FALZZGPT v12 - TAMPILAN SAMA JBALWIKOBRA + BEBAS ERROR
# ==================================================

import streamlit as st
import uuid
from datetime import datetime, timedelta
import json
import os

# --------------------------
# KONFIGURASI AWAL (Sudah diperbaiki tanda kutip)
# --------------------------
st.set_page_config(
    page_title="JB Alwi Kobra - Store Gaming",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🎮"
)

# Data Toko & Produk
INFO_TOKO = {
    "nama": "JB Alwi Kobra",
    "tagline": "Jual, Beli & Rental Akun Game Premium",
    "deskripsi": "Pusat akun gaming nomor 1 di Indonesia",
    "wa": "6282126192638",
    "rekening": "DANA / GoPay / OVO / BCA"
}

PRODUK = {
    "Free Fire": [
        {"nama": "FREEFIRE C58", "harga": 4999000, "diskon": 4300000, "status": "HOT", "kategori": "Premium"},
        {"nama": "FREE FIRE 629 I", "harga": 14599999, "diskon": 14000000, "status": "HOT", "kategori": "Premium"},
        {"nama": "FREE FIRE N217", "harga": 7500000, "diskon": 7000000, "status": "HOT", "kategori": "Reguler"},
        {"nama": "FREE FIRE N264", "harga": 17000000, "diskon": 16500000, "status": "HOT", "kategori": "Premium"},
        {"nama": "FREE FIRE 674 i", "harga": 1500000, "diskon": 1500000, "status": "Terjual", "kategori": "Pelajar"},
        {"nama": "FREE FIRE N480", "harga": 1400000, "diskon": 1400000, "status": "Terjual", "kategori": "Pelajar"},
        {"nama": "FREE FIRE N468", "harga": 1000000, "diskon": 1000000, "status": "Tersedia", "kategori": "Pelajar"},
        {"nama": "FREE FIRE N475", "harga": 1300000, "diskon": 1300000, "status": "Tersedia", "kategori": "Pelajar"},
        {"nama": "FREE FIRE N474", "harga": 1250000, "diskon": 1250000, "status": "Tersedia", "kategori": "Pelajar"},
        {"nama": "FREE FIRE N473", "harga": 1600000, "diskon": 1600000, "status": "Tersedia", "kategori": "Reguler"}
    ],
    "MLBB": [
        {"nama": "MOBILE LEGEND R152", "harga": 1800000, "diskon": 1800000, "status": "Tersedia", "kategori": "Reguler"},
        {"nama": "MOBILE LEGEND R151", "harga": 2300000, "diskon": 2300000, "status": "Tersedia", "kategori": "Reguler"}
    ],
    "Rental Akun": [
        {"nama": "FREE FIRE RENTAL 35", "harga": 30000, "durasi": "1 Jam / 2 Jam", "status": "Tersedia", "kategori": "Reguler"},
        {"nama": "FREE FIRE RENTAL 34", "harga": 30000, "durasi": "1 Jam / 2 Jam", "status": "Tersedia", "kategori": "Reguler"},
        {"nama": "FREE FIRE RENTAL 33", "harga": 30000, "durasi": "1 Jam / 2 Jam", "status": "Tersedia", "kategori": "Reguler"},
        {"nama": "FREE FIRE RENTAL 32", "harga": 25000, "durasi": "1 Jam / 2 Jam", "status": "Tersedia", "kategori": "Pelajar"}
    ]
}

# Sistem Akun & Saldo
KEY_DEVELOPER = "FALLSTORE01"
BIAYA_DAFTAR_ADMIN = 50000
MIN_TOPUP = 5000
MIN_PENARIKAN = 10000

JENIS_AKUN = ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1", "DEVELOPER"]
STATUS_AKUN = ["Belum Diverifikasi", "Aktif", "Habis Masa Aktif", "Diblokir"]

# --------------------------
# ✅ SISTEM PENYIMPANAN DATA STABIL
# --------------------------
def muat_data():
    if "daftar_akun" not in st.session_state:
        if os.path.exists("data_akun.json"):
            try:
                with open("data_akun.json", "r", encoding="utf-8") as f:
                    st.session_state.daftar_akun = json.load(f)
            except:
                st.session_state.daftar_akun = []
        else:
            st.session_state.daftar_akun = []
    return st.session_state.daftar_akun

def simpan_data(data):
    st.session_state.daftar_akun = data
    try:
        with open("data_akun.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

# --------------------------
# ✅ TAMPILAN CSS SAMA SEPERTI JBALWIKOBRA
# --------------------------
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}
body {
    background-color: #f8f9fa;
    color: #222;
}
.header {
    background: #1a1a2e;
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 0 0 15px 15px;
    margin-bottom: 20px;
}
.header h1 {
    font-size: 32px;
    margin-bottom: 5px;
}
.header p {
    font-size: 16px;
    opacity: 0.9;
}
.menu-bar {
    background: #e94560;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 25px;
    text-align: center;
}
.menu-bar a {
    color: white;
    font-weight: bold;
    text-decoration: none;
    margin: 0 15px;
    font-size: 16px;
}
.menu-bar a:hover {
    text-decoration: underline;
}
.card-produk {
    background: white;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 5px solid #e94560;
}
.harga-asli {
    text-decoration: line-through;
    color: #888;
    font-size: 15px;
}
.harga-diskon {
    font-size: 20px;
    font-weight: bold;
    color: #e94560;
    margin: 5px 0;
}
.label-status {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-bottom: 8px;
}
.status-hot {background: #ff4444; color: white;}
.status-terjual {background: #888; color: white;}
.status-tersedia {background: #00C853; color: white;}
.btn-wa {
    background: #25D366;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    margin-top: 8px;
}
.btn-wa:hover {
    background: #128C7E;
    color: white;
}
.login-box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 20px auto;
}
.info-saldo {
    background: #fef3c7;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
    text-align: center;
    font-weight: bold;
    color: #92400e;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# INISIALISASI SESI
# --------------------------
if "login" not in st.session_state:
    st.session_state.login = False
if "data_akun" not in st.session_state:
    st.session_state.data_akun = None

# --------------------------
# HALAMAN UTAMA
# --------------------------
def halaman_utama():
    # Header
    st.markdown(f"""
    <div class="header">
        <h1>🎮 {INFO_TOKO['nama']}</h1>
        <p>{INFO_TOKO['tagline']}</p>
        <small>{INFO_TOKO['deskripsi']}</small>
    </div>
    """, unsafe_allow_html=True)

    # Menu Navigasi
    st.markdown(f"""
    <div class="menu-bar">
        <a href="#produk">📦 Stok Akun</a>
        <a href="#rental">🔄 Rental Akun</a>
        <a href="#kontak">📞 Kontak Kami</a>
        <a href="#akun">👤 Akun Saya</a>
    </div>
    """, unsafe_allow_html=True)

    # Info Diskon
    if datetime.now().weekday() in (5,6):
        st.markdown("""
        <div style='background: #ff9800; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 15px 0;'>
        🎉 DISKON TAMBAHAN 20% SETIAP SABTU & MINGGU! 🎉
        </div>
        """, unsafe_allow_html=True)

    # Tampilkan Produk per Kategori
    st.markdown("<h2 id='produk' style='color:#1a1a2e; margin:30px 0 15px;'>🔥 Stok Akun Terbaru</h2>", unsafe_allow_html=True)

    for kategori, daftar in PRODUK.items():
        if kategori != "Rental Akun":
            st.markdown(f"<h3 style='color:#e94560; margin:20px 0 10px;'>🎮 {kategori}</h3>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, item in enumerate(daftar):
                with cols[i%2]:
                    label = "label-status status-" + item["status"].lower()
                    st.markdown(f"""
                    <div class="card-produk">
                        <span class="{label}">{item['status']}</span>
                        <h4>{item['nama']}</h4>
                        <p class="harga-asli">Rp {item['harga']:,}</p>
                        <p class="harga-diskon">Rp {item['diskon']:,}</p>
                        <p>Kategori: {item['kategori']}</p>
                        <a class="btn-wa" href="https://wa.me/{INFO_TOKO['wa']}?text=Halo%20Saya%20Mau%20Pesan%20{item['nama']}" target="_blank">💬 Pesan via WhatsApp</a>
                    </div>
                    """, unsafe_allow_html=True)

    # Bagian Rental
    st.markdown("<h2 id='rental' style='color:#1a1a2e; margin:30px 0 15px;'>🔄 Rental Akun</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, item in enumerate(PRODUK["Rental Akun"]):
        with cols[i%2]:
            st.markdown(f"""
            <div class="card-produk">
                <span class="label-status status-tersedia">{item['status']}</span>
                <h4>{item['nama']}</h4>
                <p>Mulai Rp {item['harga']:,}</p>
                <p>Durasi: {item['durasi']}</p>
                <p>Kategori: {item['kategori']}</p>
                <a class="btn-wa" href="https://wa.me/{INFO_TOKO['wa']}?text=Halo%20Saya%20Mau%20Rental%20{item['nama']}" target="_blank">💬 Pesan via WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)

    # Kontak
    st.markdown("<h2 id='kontak' style='color:#1a1a2e; margin:30px 0 15px;'>📞 Kontak Resmi</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card-produk">
        <h4>📲 WhatsApp Resmi</h4>
        <p>Nomor: <strong>0821-2619-2638</strong></p>
        <h4>💳 Rekening Pembayaran</h4>
        <p>{INFO_TOKO['rekening']}</p>
        <p style="color:#e94560; font-weight:bold;">⚠️ Hanya percaya nomor ini! Jangan transfer ke nomor lain!</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# HALAMAN DAFTAR & MASUK
# --------------------------
def halaman_akun():
    st.markdown("<h2 id='akun' style='text-align:center; margin:20px 0;'>👤 Akun Saya</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Daftar Akun", "🔑 Masuk Akun"])

    with tab1:
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        email = st.text_input("Email")
        jenis = st.selectbox("Daftar Sebagai", JENIS_AKUN)

        kunci_dev = ""
        bisa = True
        if jenis == "DEVELOPER":
            kunci_dev = st.text_input("Kunci Developer", type="password")
            if kunci_dev != KEY_DEVELOPER:
                st.warning("⚠️ Kunci salah!")
                bisa = False

        if st.button("📝 Kirim Pendaftaran", type="primary", use_container_width=True, disabled=not bisa):
            if nama and hp and email:
                daftar = muat_data()
                if any(a["hp"] == hp for a in daftar):
                    st.error("❌ Nomor HP sudah terdaftar!")
                    return

                akun_baru = {
                    "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                    "nama": nama,
                    "hp": hp,
                    "email": email,
                    "jenis": jenis,
                    "status": "Aktif" if jenis == "DEVELOPER" else "Belum Diverifikasi",
                    "saldo": 9999999 if jenis == "DEVELOPER" else 0,
                    "tgl_daftar": datetime.now().isoformat()
                }
                daftar.append(akun_baru)
                simpan_data(daftar)
                st.success(f"✅ Berhasil! ID Akun: {akun_baru['id']}")
            else:
                st.warning("⚠️ Lengkapi semua data!")

    with tab2:
        id_masuk = st.text_input("ID Akun / Nomor HP")
        kunci_masuk = st.text_input("Kunci Khusus (Developer)", type="password", placeholder="Kosongkan jika bukan")

        if st.button("🔑 Masuk Sekarang", type="primary", use_container_width=True):
            daftar = muat_data()
            akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)

            if not akun:
                st.error("❌ Akun tidak ditemukan!")
                return

            if akun["jenis"] == "DEVELOPER" and kunci_masuk != KEY_DEVELOPER:
                st.error("❌ Kunci salah!")
                return

            if akun["status"] != "Aktif":
                st.warning("⚠️ Belum diverifikasi!")
                return

            st.session_state.login = True
            st.session_state.data_akun = akun
            st.rerun()

# --------------------------
# HALAMAN DASHBOARD SETELAH MASUK
# --------------------------
def halaman_dashboard():
    akun = st.session_state.data_akun
    st.markdown(f"""
    <div class="header">
        <h1>👋 Selamat Datang, {akun['nama']}</h1>
        <p>Jenis Akun: {akun['jenis']} | Status: {akun['status']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-saldo">
        💰 Saldo Anda: Rp {akun['saldo']:,}
    </div>
    """, unsafe_allow_html=True)

    menu = ["🛒 Kembali ke Toko", "💎 Top Up Saldo", "💸 Penarikan", "👤 Profil", "🚪 Keluar"]
    if akun["jenis"] in ["ADMIN_1", "DEVELOPER"]:
        menu.insert(2, "✅ Verifikasi Akun")
    if akun["jenis"] == "DEVELOPER":
        menu.append("⚙️ Kelola Produk")

    pilih = st.sidebar.selectbox("📋 Menu Admin", menu)

    if pilih == "🚪 Keluar":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()
    elif pilih == "✅ Verifikasi Akun":
        daftar = muat_data()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"ID: {a['id']} | Nama: {a['nama']} | HP: {a['hp']}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=f"aktif_{a['id']}"):
                    a["status"] = "Aktif"
                    simpan_data(daftar)
                    st.success("✅ Diaktifkan!")
                    st.rerun()
        else:
            st.info("Tidak ada akun menunggu verifikasi")
    elif pilih == "💎 Top Up Saldo":
        nominal = st.number_input("Jumlah Isi Saldo", min_value=MIN_TOPUP, step=5000)
        if st.button("Kirim Permintaan"):
            akun["saldo"] += nominal
            simpan_data(muat_data())
            st.success(f"✅ Permintaan terkirim! Setelah konfirmasi, saldo akan bertambah Rp{nominal:,}")
    elif pilih == "💸 Penarikan":
        if akun["saldo"] < MIN_PENARIKAN:
            st.warning(f"Minimal tarik Rp{MIN_PENARIKAN:,}")
        else:
            jumlah = st.number_input("Jumlah Tarik", min_value=MIN_PENARIKAN, max_value=akun["saldo"])
            metode = st.selectbox("Metode", ["DANA", "GoPay", "OVO", "BCA"])
            nomor = st.text_input("Nomor Tujuan")
            if st.button("Kirim"):
                akun["saldo"] -= jumlah
                simpan_data(muat_data())
                st.success(f"✅ Permintaan diproses! Rp{jumlah:,} akan dikirim ke {metode}")
    elif pilih == "👤 Profil":
        st.json(akun)
    elif pilih == "🛒 Kembali ke Toko":
        halaman_utama()

# --------------------------
# JALANKAN SISTEM
# --------------------------
if not st.session_state.login:
    halaman_utama()
    halaman_akun()
else:
    halaman_dashboard()

# --------------------------
# ✅ SISTEM PENYIMPANAN DATA STABIL
# --------------------------
def muat_data():
    if "daftar_akun" not in st.session_state:
        if os.path.exists("data_akun.json"):
            try:
                with open("data_akun.json", "r", encoding="utf-8") as f:
                    st.session_state.daftar_akun = json.load(f)
            except:
                st.session_state.daftar_akun = []
        else:
            st.session_state.daftar_akun = []
    return st.session_state.daftar_akun

def simpan_data(data):
    st.session_state.daftar_akun = data
    try:
        with open("data_akun.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

# --------------------------
# ✅ TAMPILAN CSS SAMA SEPERTI JBALWIKOBRA
# --------------------------
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}
body {
    background-color: #f8f9fa;
    color: #222;
}
.header {
    background: #1a1a2e;
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 0 0 15px 15px;
    margin-bottom: 20px;
}
.header h1 {
    font-size: 32px;
    margin-bottom: 5px;
}
.header p {
    font-size: 16px;
    opacity: 0.9;
}
.menu-bar {
    background: #e94560;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 25px;
    text-align: center;
}
.menu-bar a {
    color: white;
    font-weight: bold;
    text-decoration: none;
    margin: 0 15px;
    font-size: 16px;
}
.menu-bar a:hover {
    text-decoration: underline;
}
.card-produk {
    background: white;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 5px solid #e94560;
}
.harga-asli {
    text-decoration: line-through;
    color: #888;
    font-size: 15px;
}
.harga-diskon {
    font-size: 20px;
    font-weight: bold;
    color: #e94560;
    margin: 5px 0;
}
.label-status {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-bottom: 8px;
}
.status-hot {background: #ff4444; color: white;}
.status-terjual {background: #888; color: white;}
.status-tersedia {background: #00C853; color: white;}
.btn-wa {
    background: #25D366;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    margin-top: 8px;
}
.btn-wa:hover {
    background: #128C7E;
    color: white;
}
.login-box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 20px auto;
}
.info-saldo {
    background: #fef3c7;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
    text-align: center;
    font-weight: bold;
    color: #92400e;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# INISIALISASI SESI
# --------------------------
if "login" not in st.session_state:
    st.session_state.login = False
if "data_akun" not in st.session_state:
    st.session_state.data_akun = None

# --------------------------
# HALAMAN UTAMA
# --------------------------
def halaman_utama():
    # Header
    st.markdown(f"""
    <div class="header">
        <h1>🎮 {INFO_TOKO['nama']}</h1>
        <p>{INFO_TOKO['tagline']}</p>
        <small>{INFO_TOKO['deskripsi']}</small>
    </div>
    """, unsafe_allow_html=True)

    # Menu Navigasi
    st.markdown(f"""
    <div class="menu-bar">
        <a href="#produk">📦 Stok Akun</a>
        <a href="#rental">🔄 Rental Akun</a>
        <a href="#topup">💳 Top Up Game</a>
        <a href="#kontak">📞 Kontak Kami</a>
        <a href="#akun">👤 Akun Saya</a>
    </div>
    """, unsafe_allow_html=True)

    # Info Diskon
    if datetime.now().weekday() in (5,6):
        st.markdown("""
        <div style='background: #ff9800; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 15px 0;'>
        🎉 DISKON TAMBAHAN 20% SETIAP SABTU & MINGGU! 🎉
        </div>
        """, unsafe_allow_html=True)

    # Tampilkan Produk per Kategori
    st.markdown("<h2 id='produk' style='color:#1a1a2e; margin:30px 0 15px;'>🔥 Stok Akun Terbaru</h2>", unsafe_allow_html=True)

    for kategori, daftar in PRODUK.items():
        if kategori != "Rental Akun":
            st.markdown(f"<h3 style='color:#e94560; margin:20px 0 10px;'>🎮 {kategori}</h3>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, item in enumerate(daftar):
                with cols[i%2]:
                    label = "label-status status-" + item["status"].lower()
                    st.markdown(f"""
                    <div class="card-produk">
                        <span class="{label}">{item['status']}</span>
                        <h4>{item['nama']}</h4>
                        <p class="harga-asli">Rp {item['harga']:,}</p>
                        <p class="harga-diskon">Rp {item['diskon']:,}</p>
                        <p>Kategori: {item['kategori']}</p>
                        <a class="btn-wa" href="https://wa.me/{INFO_TOKO['wa']}?text=Halo%20Saya%20Mau%20Pesan%20{item['nama']}" target="_blank">💬 Pesan via WhatsApp</a>
                    </div>
                    """, unsafe_allow_html=True)

    # Bagian Rental
    st.markdown("<h2 id='rental' style='color:#1a1a2e; margin:30px 0 15px;'>🔄 Rental Akun</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, item in enumerate(PRODUK["Rental Akun"]):
        with cols[i%2]:
            st.markdown(f"""
            <div class="card-produk">
                <span class="label-status status-tersedia">{item['status']}</span>
                <h4>{item['nama']}</h4>
                <p>Mulai Rp {item['harga']:,}</p>
                <p>Durasi: {item['durasi']}</p>
                <p>Kategori: {item['kategori']}</p>
                <a class="btn-wa" href="https://wa.me/{INFO_TOKO['wa']}?text=Halo%20Saya%20Mau%20Rental%20{item['nama']}" target="_blank">💬 Pesan via WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)

    # Kontak
    st.markdown("<h2 id='kontak' style='color:#1a1a2e; margin:30px 0 15px;'>📞 Kontak Resmi</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card-produk">
        <h4>📲 WhatsApp Resmi</h4>
        <p>Nomor: <strong>0821-2619-2638</strong></p>
        <h4>💳 Rekening Pembayaran</h4>
        <p>{INFO_TOKO['rekening']}</p>
        <p style="color:#e94560; font-weight:bold;">⚠️ Hanya percaya nomor ini! Jangan transfer ke nomor lain!</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# HALAMAN DAFTAR & MASUK
# --------------------------
def halaman_akun():
    st.markdown("<h2 id='akun' style='text-align:center; margin:20px 0;'>👤 Akun Saya</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Daftar Akun", "🔑 Masuk Akun"])

    with tab1:
        with st.container():
            nama = st.text_input("Nama Lengkap")
            hp = st.text_input("Nomor HP")
            email = st.text_input("Email")
            jenis = st.selectbox("Daftar Sebagai", JENIS_AKUN)

            kunci_dev = ""
            bisa = True
            if jenis == "DEVELOPER":
                kunci_dev = st.text_input("Kunci Developer", type="password")
                if kunci_dev != KEY_DEVELOPER:
                    st.warning("⚠️ Kunci salah!")
                    bisa = False

            if st.button("📝 Kirim Pendaftaran", type="primary", use_container_width=True, disabled=not bisa):
                if nama and hp and email:
                    daftar = muat_data()
                    if any(a["hp"] == hp for a in daftar):
                        st.error("❌ Nomor HP sudah terdaftar!")
                        return

                    akun_baru = {
                        "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                        "nama": nama,
                        "hp": hp,
                        "email": email,
                        "jenis": jenis,
                        "status": "Aktif" if jenis == "DEVELOPER" else "Belum Diverifikasi",
                        "saldo": 9999999 if jenis == "DEVELOPER" else 0,
                        "tgl_daftar": datetime.now().isoformat()
                    }
                    daftar.append(akun_baru)
                    simpan_data(daftar)
                    st.success(f"✅ Berhasil! ID Akun: {akun_baru['id']}")
                else:
                    st.warning("⚠️ Lengkapi semua data!")

    with tab2:
        with st.container():
            id_masuk = st.text_input("ID Akun / Nomor HP")
            kunci_masuk = st.text_input("Kunci Khusus (Developer)", type="password", placeholder="Kosongkan jika bukan")

            if st.button("🔑 Masuk Sekarang", type="primary", use_container_width=True):
                daftar = muat_data()
                akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)

                if not akun:
                    st.error("❌ Akun tidak ditemukan!")
                    return

                if akun["jenis"] == "DEVELOPER" and kunci_masuk != KEY_DEVELOPER:
                    st.error("❌ Kunci salah!")
                    return

                if akun["status"] != "Aktif":
                    st.warning("⚠️ Belum diverifikasi!")
                    return

                st.session_state.login = True
                st.session_state.data_akun = akun
                st.rerun()

# --------------------------
# HALAMAN DASHBOARD SETELAH MASUK
# --------------------------
def halaman_dashboard():
    akun = st.session_state.data_akun
    st.markdown(f"""
    <div class="header">
        <h1>👋 Selamat Datang, {akun['nama']}</h1>
        <p>Jenis Akun: {akun['jenis']} | Status: {akun['status']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-saldo">
        💰 Saldo Anda: Rp {akun['saldo']:,}
    </div>
    """, unsafe_allow_html=True)

    menu = ["🛒 Kembali ke Toko", "💎 Top Up Saldo", "💸 Penarikan", "👤 Profil", "🚪 Keluar"]
    if akun["jenis"] in ["ADMIN_1", "DEVELOPER"]:
        menu.insert(2, "✅ Verifikasi Akun")
    if akun["jenis"] == "DEVELOPER":
        menu.append("⚙️ Kelola Produk")

    pilih = st.sidebar.selectbox("📋 Menu Admin", menu)

    if pilih == "🚪 Keluar":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()
    elif pilih == "✅ Verifikasi Akun":
        daftar = muat_data()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"ID: {a['id']} | Nama: {a['nama']} | HP: {a['hp']}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=f"aktif_{a['id']}"):
                    a["status"] = "Aktif"
                    simpan_data(daftar)
                    st.success("✅ Diaktifkan!")
                    st.rerun()
        else:
            st.info("Tidak ada akun menunggu verifikasi")
    elif pilih == "💎 Top Up Saldo":
        nominal = st.number_input("Jumlah Isi Saldo", min_value=MIN_TOPUP, step=5000)
        if st.button("Kirim Permintaan"):
            akun["saldo"] += nominal
            simpan_data(muat_data())
            st.success(f"✅ Permintaan terkirim! Setelah konfirmasi, saldo akan bertambah Rp{nominal:,}")
    elif pilih == "💸 Penarikan":
        if akun["saldo"] < MIN_PENARIKAN:
            st.warning(f"Minimal tarik Rp{MIN_PENARIKAN:,}")
        else:
            jumlah = st.number_input("Jumlah Tarik", min_value=MIN_PENARIKAN, max_value=akun["saldo"])
            metode = st.selectbox("Metode", ["DANA", "GoPay", "OVO", "BCA"])
            nomor = st.text_input("Nomor Tujuan")
            if st.button("Kirim"):
                akun["saldo"] -= jumlah
                simpan_data(muat_data())
                st.success(f"✅ Permintaan diproses! Rp{jumlah:,} akan dikirim ke {metode}")
    elif pilih == "👤 Profil":
        st.json(akun)
    elif pilih == "🛒 Kembali ke Toko":
        halaman_utama()

# --------------------------
# JALANKAN SISTEM
# --------------------------
if not st.session_state.login:
    halaman_utama()
    halaman_akun()
else:
    halaman_dashboard()
