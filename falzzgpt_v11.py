# ==================================================
# FALZZGPT v11.1 - VERSI FINAL: FIX ERROR + SISTEM LANGGANAN BERJALAN
# ==================================================

import streamlit as st
import uuid
from datetime import datetime, timedelta
import json
import os
import hashlib
import requests

# --------------------------
# KONFIGURASI DASAR
# --------------------------
st.set_page_config(
    page_title="FalzzGPT v11 | Ultimate Fortress",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

VERSI = "11.1 FINAL"
KEY_DEVELOPER = "FALLSTORE01"
BIAYA_DAFTAR_ADMIN = 50000
MIN_TOPUP = 5000
MIN_PENARIKAN = 10000

# ✅ DAFTAR PAKET DENGAN HARGA & DURASI
DAFTAR_PAKET = {
    "PERCOBAAN": {
        "nama": "Paket Percobaan (7 Hari)",
        "harga": 0,
        "durasi": 7,
        "keterangan": "Gratis untuk pengguna baru"
    },
    "BULANAN": {
        "nama": "Paket Bulanan",
        "harga": 15000,
        "durasi": 30,
        "keterangan": "Akses penuh selama 30 hari"
    },
    "TAHUNAN": {
        "nama": "Paket Tahunan",
        "harga": 35000,
        "durasi": 365,
        "keterangan": "Hemat 35% dibandingkan bulanan"
    },
    "PERMANEN": {
        "nama": "Paket Permanen ✅",
        "harga": 50000,
        "durasi": 99999,
        "keterangan": "Akses selamanya tanpa batas waktu"
    }
}

JENIS_AKUN = ["PENGGUNA", "ADMIN_3", "ADMIN_2", "ADMIN_1", "DEVELOPER"]
STATUS_AKUN = ["Belum Diverifikasi", "Aktif", "Habis Masa Aktif", "Diblokir"]

# --------------------------
# ✅ SISTEM PENYIMPANAN DATA AMAN
# --------------------------
def muat_semua_data():
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

def simpan_semua_data(data):
    st.session_state.daftar_akun = data
    try:
        with open("data_akun.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

# --------------------------
# ✅ FUNGSI BANTU
# --------------------------
def cek_masa_aktif(akun):
    tgl_akhir = datetime.fromisoformat(akun["tgl_berakhir"])
    if tgl_akhir < datetime.now():
        akun["status"] = "Habis Masa Aktif"
    return akun

# --------------------------
# TAMPILAN UTAMA & CSS
# --------------------------
st.markdown("""
<style>
* {font-family: 'Segoe UI', Roboto, sans-serif; margin:0; padding:0; box-sizing:border-box;}
body {background: #0F1117; color: #E0E6ED;}
.card {background: #1A1C23; border-radius: 14px; padding: 22px; margin-bottom: 20px; border: 1px solid #2A2D38;}
h1 {color: #4D90FE; text-align: center; font-size: 30px; font-weight: bold;}
h2 {color: #E0E6ED; font-size: 22px;}
.stButton>button {width: 100%; border-radius: 8px; font-weight: 600; padding: 8px;}
.btn-primary {background: #4D90FE; border: none; color: white;}
.btn-danger {background: #E53E3E; border: none; color: white;}
.info-box {background: #232630; padding: 12px; border-radius: 8px; margin: 8px 0;}
</style>
""", unsafe_allow_html=True)

# Inisialisasi sesi
if "login" not in st.session_state:
    st.session_state.login = False
if "data_akun" not in st.session_state:
    st.session_state.data_akun = None

# --------------------------
# HALAMAN LOGIN & DAFTAR
# --------------------------
if not st.session_state.login:
    st.markdown("<div class='card'><h1>🛡️ FALZZGPT v11.1</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Daftar Akun", "🔑 Masuk Akun"])

    with tab1:
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP (aktif)")
        email = st.text_input("Email")
        jenis = st.selectbox("Daftar Sebagai", JENIS_AKUN)
        paket = st.selectbox("Pilih Paket Berlangganan", list(DAFTAR_PAKET.keys()), format_func=lambda x: DAFTAR_PAKET[x]["nama"])

        kunci_dev = ""
        bisa_daftar = True
        if jenis == "DEVELOPER":
            kunci_dev = st.text_input("Masukkan Kunci Developer", type="password", help="Contoh: FALLSTORE01")
            if kunci_dev != KEY_DEVELOPER:
                st.warning("⚠️ Kunci Developer tidak cocok!")
                bisa_daftar = False
        elif jenis != "PENGGUNA":
            st.info(f"ℹ️ Biaya pendaftaran sebagai {jenis}: Rp{BIAYA_DAFTAR_ADMIN:,}")

        if st.button("Kirim Pendaftaran", type="primary", use_container_width=True, disabled=not bisa_daftar):
            if not nama or not hp or not email:
                st.warning("⚠️ Lengkapi semua data terlebih dahulu!")
                st.stop()

            daftar = muat_semua_data()
            if any(a["hp"] == hp for a in daftar):
                st.error("❌ Nomor HP sudah terdaftar!")
                st.stop()

            # Tentukan status & saldo awal
            if jenis == "DEVELOPER":
                status = "Aktif"
                saldo = 9999999
            elif jenis == "PENGGUNA":
                status = "Aktif" if DAFTAR_PAKET[paket]["harga"] == 0 else "Belum Diverifikasi"
                saldo = 0
            else:
                status = "Belum Diverifikasi"
                saldo = BIAYA_DAFTAR_ADMIN

            tgl_akhir = datetime.now() + timedelta(days=DAFTAR_PAKET[paket]["durasi"])

            akun_baru = {
                "id": f"FLZ-{uuid.uuid4().hex[:8].upper()}",
                "nama": nama,
                "hp": hp,
                "email": email,
                "jenis": jenis,
                "paket": paket,
                "status": status,
                "saldo": saldo,
                "tgl_daftar": datetime.now().isoformat(),
                "tgl_berakhir": tgl_akhir.isoformat()
            }

            daftar.append(akun_baru)
            simpan_semua_data(daftar)

            if jenis == "DEVELOPER":
                st.success(f"""✅ **PENDAFTARAN BERHASIL!**
                • ID Akun: `{akun_baru['id']}`
                • Status: **Langsung Aktif**
                • Saldo Awal: Rp{saldo:,}
                Silakan masuk menggunakan ID atau Nomor HP kamu!""")
            else:
                st.success("✅ Data terkirim! Akun akan aktif setelah pembayaran & verifikasi.")

    with tab2:
        st.info("Bisa masuk pakai **ID Akun** atau **Nomor HP**")
        id_masuk = st.text_input("ID Akun / Nomor HP")
        kunci_masuk = st.text_input("Kunci Khusus (hanya Developer)", type="password", placeholder="Kosongkan jika bukan Developer")

        if st.button("Masuk Sekarang", type="primary", use_container_width=True):
            daftar = muat_semua_data()
            akun = next((a for a in daftar if a["id"] == id_masuk or a["hp"] == id_masuk), None)

            if not akun:
                st.error("❌ Akun tidak ditemukan! Cek kembali data pendaftaran.")
                st.stop()

            akun = cek_masa_aktif(akun)
            if akun["jenis"] == "DEVELOPER" and kunci_masuk != KEY_DEVELOPER:
                st.error("❌ Kunci Developer salah!")
                st.stop()
            if akun["status"] != "Aktif":
                st.warning(f"⚠️ Status akun: {akun['status']}. Tidak bisa masuk.")
                st.stop()

            st.session_state.login = True
            st.session_state.data_akun = akun
            st.rerun()

# --------------------------
# HALAMAN UTAMA SETELAH MASUK
# --------------------------
else:
    akun = cek_masa_aktif(st.session_state.data_akun)
    daftar = muat_semua_data()
    sisa_hari = max(0, (datetime.fromisoformat(akun["tgl_berakhir"]) - datetime.now()).days)

    # Info diskon akhir pekan
    if datetime.now().weekday() in (5,6):
        st.markdown("""
        <div style='background: linear-gradient(90deg, #FFB700, #FF8800); color: white; padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px;'>
        🎉 DISKON 20% SETIAP SABTU & MINGGU! 🎉
        </div>
        """, unsafe_allow_html=True)

    # Menu sesuai hak akses
    menu = ["👤 Profil Saya", "💳 Berlangganan", "💎 Top Up Saldo", "🤖 AI Asisten", "📚 Belajar Koding", "💸 Penarikan", "🚪 Keluar"]
    if akun["jenis"] in ["ADMIN_1", "DEVELOPER"]:
        menu.insert(2, "✅ Verifikasi Akun")
    if akun["jenis"] == "DEVELOPER":
        menu.extend(["👥 Kelola Pengguna", "📊 Laporan Transaksi", "⚙️ Pengaturan Sistem"])

    menu_pilih = st.sidebar.selectbox("📋 MENU UTAMA", menu)

    # Info akun di samping
    st.sidebar.markdown(f"""
    <div class='info-box'>
    <h4>📊 DATA AKUN</h4>
    • Nama: {akun['nama']}
    • Jenis: <span style='color:#4D90FE; font-weight:bold;'>{akun['jenis']}</span>
    • Paket: {DAFTAR_PAKET[akun['paket']]['nama']}
    • Sisa Masa Aktif: {sisa_hari} Hari
    • Saldo: <span style='color:#00C853; font-weight:bold;'>Rp {akun['saldo']:,}</span>
    • Status: <span style='color:#00C853;'>{akun['status']}</span>
    </div>
    """, unsafe_allow_html=True)

    if menu_pilih == "🚪 Keluar":
        st.session_state.login = False
        st.session_state.data_akun = None
        st.rerun()

    elif menu_pilih == "👤 Profil Saya":
        st.markdown("<div class='card'><h2>👤 Profil Lengkap</h2></div>", unsafe_allow_html=True)
        st.json(akun)

    elif menu_pilih == "💳 Berlangganan":
        st.markdown("<div class='card'><h2>💳 Pilih & Perpanjang Langganan</h2></div>", unsafe_allow_html=True)
        diskon = 0.8 if datetime.now().weekday() in (5,6) else 1.0

        for kode, paket in DAFTAR_PAKET.items():
            harga_akhir = int(paket["harga"] * diskon)
            st.markdown(f"""
            <div class='info-box'>
            <h4>{paket['nama']}</h4>
            <p>{paket['keterangan']}</p>
            <p>💰 Harga: Rp{harga_akhir:,} {'<small style="color:#FFB700;">(Diskon 20%)</small>' if diskon < 1 else ''}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Beli Paket {kode}", key=f"beli_{kode}"):
                if akun["saldo"] >= harga_akhir:
                    akun["saldo"] -= harga_akhir
                    akun["paket"] = kode
                    akun["tgl_berakhir"] = (datetime.now() + timedelta(days=paket["durasi"])).isoformat()
                    akun["status"] = "Aktif"
                    simpan_semua_data(daftar)
                    st.session_state.data_akun = akun
                    st.success(f"✅ Berhasil! Paket {paket['nama']} aktif sampai {akun['tgl_berakhir'][:10]}")
                    st.rerun()
                else:
                    st.error(f"❌ Saldo tidak cukup! Kurang Rp{harga_akhir - akun['saldo']:,}")

    elif menu_pilih == "✅ Verifikasi Akun":
        st.markdown("<div class='card'><h2>✅ Verifikasi Pendaftaran</h2></div>", unsafe_allow_html=True)
        daftar = muat_semua_data()
        belum = [a for a in daftar if a["status"] == "Belum Diverifikasi"]
        if belum:
            for a in belum:
                st.write(f"**ID:** {a['id']} | **Nama:** {a['nama']} | **Jenis:** {a['jenis']} | **Saldo:** Rp{a['saldo']:,}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Aktifkan", key=f"aktif_{a['id']}"):
                    a["status"] = "Aktif"
                    simpan_semua_data(daftar)
                    st.success("✅ Akun diaktifkan!")
                    st.rerun()
                if col2.button("❌ Tolak & Hapus", key=f"tolak_{a['id']}"):
                    daftar.remove(a)
                    simpan_semua_data(daftar)
                    st.info("❌ Pendaftaran ditolak")
                    st.rerun()
        else:
            st.info("Tidak ada akun yang menunggu verifikasi")

    elif menu_pilih == "💎 Top Up Saldo":
        st.markdown("<div class='card'><h2>💎 Isi Ulang Saldo</h2></div>", unsafe_allow_html=True)
        nominal = st.number_input("Masukkan Jumlah", min_value=MIN_TOPUP, step=5000, value=10000)
        if st.button("Kirim Permintaan Top Up", type="primary"):
            st.success(f"""✅ Permintaan terkirim!
            • Nominal: Rp{nominal:,}
            • Silakan transfer ke nomor rekening/WA admin untuk konfirmasi""")

    elif menu_pilih == "🤖 AI Asisten":
        st.markdown("<div class='card'><h2>🤖 AI Asisten Pintar</h2></div>", unsafe_allow_html=True)
        pesan = st.text_area("Tanya apa saja, minta kode, atau buat konten...", height=150)
        if st.button("Kirim ke AI", type="primary"):
            if pesan.strip():
                st.info(f"💬 Jawaban untuk: {pesan[:70]}...")
                st.success("✅ Pesan diproses! Fitur jawaban AI bisa disambungkan ke API nanti.")
            else:
                st.warning("⚠️ Masukkan pertanyaan terlebih dahulu!")

    elif menu_pilih == "📚 Belajar Koding":
        st.markdown("<div class='card'><h2>📚 Pusat Belajar Pemrograman</h2></div>", unsafe_allow_html=True)
        bahasa = st.selectbox("Pilih Bahasa", ["Python", "JavaScript", "HTML & CSS", "PHP", "Java", "C++"])
        st.info(f"Materi dasar, contoh kode, dan panduan belajar **{bahasa}** tersedia untuk kamu.")

    elif menu_pilih == "💸 Penarikan":
        st.markdown("<div class='card'><h2>💸 Tarik Saldo</h2></div>", unsafe_allow_html=True)
        if akun["saldo"] < MIN_PENARIKAN:
            st.warning(f"⚠️ Minimal penarikan Rp{MIN_PENARIKAN:,} | Saldo kamu: Rp{akun['saldo']:,}")
        else:
            jumlah = st.number_input("Jumlah Tarik", min_value=MIN_PENARIKAN, max_value=akun["saldo"], step=5000)
            metode = st.selectbox("Metode Penarikan", ["DANA", "GoPay", "OVO", "Rekening Bank"])
            nomor = st.text_input("Nomor Tujuan")
            if st.button("Kirim Permintaan Tarik", type="primary"):
                akun["saldo"] -= jumlah
                simpan_semua_data(daftar)
                st.success(f"✅ Permintaan terkirim! Rp{jumlah:,} akan diproses ke {metode} - {nomor}")
