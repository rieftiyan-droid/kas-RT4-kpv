import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nama file database sederhana (CSV)
FILE_DB = 'data_iuran_rt.csv'

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(FILE_DB):
        return pd.read_csv(FILE_DB)
    else:
        return pd.DataFrame(columns=["Tanggal", "Nama Warga", "Blok/No", "Bulan Iuran", "Nominal", "Keterangan"])

# Fungsi untuk menyimpan data
def save_data(df):
    df.to_csv(FILE_DB, index=False)

# --- TAMPILAN APLIKASI ---
st.title("💰 Sistem Pencatatan Iuran Kas RT")

# Sidebar untuk Input Data
st.sidebar.header("Input Pembayaran Baru")
with st.sidebar.form("form_iuran"):
    nama = st.text_input("Nama Warga")
    blok = st.text_input("Blok / Nomor Rumah")
    bulan = st.selectbox("Bulan Iuran", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"])
    nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
    ket = st.text_area("Keterangan Tambahan")
    submitted = st.form_submit_button("Simpan Data")

    if submitted:
        if nama and nominal > 0:
            df_lama = load_data()
            data_baru = {
                "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nama Warga": nama,
                "Blok/No": blok,
                "Bulan Iuran": bulan,
                "Nominal": nominal,
                "Keterangan": ket
            }
            # Menggabungkan data baru
            df_baru = pd.concat([df_lama, pd.DataFrame([data_baru])], ignore_index=True)
            save_data(df_baru)
            st.success("Data berhasil disimpan!")
        else:
            st.error("Mohon lengkapi Nama dan Nominal.")

# Area Utama: Laporan
st.header("Rekapitulasi Kas")

df = load_data()

if not df.empty:
    # Menampilkan Tabel Data
    st.dataframe(df)

    # Menampilkan Total Saldo
    total_kas = df['Nominal'].sum()
    st.metric(label="Total Saldo Kas Saat Ini", value=f"Rp {total_kas:,.0f}")
    
    # Tombol Download Laporan
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Laporan (CSV)",
        data=csv,
        file_name='laporan_kas_rt.csv',
        mime='text/csv',
    )
else:
    st.info("Belum ada data transaksi. Silakan input di menu sebelah kiri.")