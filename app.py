import streamlit as st
from PIL import Image
import os
import pandas as pd
import altair as alt

import kripto_aes
import stego_lsb

st.set_page_config(
    page_title="SecureIjazah — Sistem Keamanan Dokumen Akademik",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  [data-testid="stSidebar"] {
    background-color: #0F172A !important;
    border-right: 1px solid #1E293B;
  }
  [data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
  }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
    color: #F1F5F9 !important;
  }

  .main-header {
    padding: 2rem 0 1.5rem 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 2rem;
  }

  .stat-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .stat-card-dark {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    color: #F1F5F9;
  }

  .section-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 1.5rem;
  }

  div[data-testid="stForm"] {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.12) !important;
  }
  div[data-testid="stForm"] label,
  div[data-testid="stForm"] p,
  div[data-testid="stForm"] span {
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
  }

  div[data-testid="stForm"] .stTextInput input,
  div[data-testid="stForm"] [data-testid="stFileUploaderDropzone"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-size: 0.9rem !important;
  }
  div[data-testid="stForm"] .stTextInput input::placeholder {
    color: #475569 !important;
  }
  div[data-testid="stForm"] .stTextInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    background-color: #0F172A !important;
  }

  div[data-testid="stForm"] hr {
    border-color: #1E293B !important;
  }

  .stButton > button[kind="primary"],
  .stFormSubmitButton > button[kind="primary"] {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.2s, transform 0.15s !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
  }
  .stButton > button[kind="primary"]:hover,
  .stFormSubmitButton > button[kind="primary"]:hover {
    background: #1D4ED8 !important;
    transform: translateY(-1px) !important;
    color: #FFFFFF !important;
  }

  .stButton > button[kind="secondary"],
  .stFormSubmitButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
  }

  .stDownloadButton > button {
    background: #059669 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: background 0.2s !important;
  }
  .stDownloadButton > button:hover {
    background: #047857 !important;
  }

  .stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #E2E8F0;
    background: transparent;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    font-size: 0.875rem;
    letter-spacing: 0.02em;
    color: #64748B;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
  }
  .stTabs [aria-selected="true"] {
    color: #2563EB !important;
    border-bottom: 2px solid #2563EB !important;
    background: transparent !important;
  }

  .stSuccess {
    border-radius: 10px;
  }

  .badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .badge-green {
    background: #ECFDF5;
    color: #065F46;
    border-color: #A7F3D0;
  }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem 0;">
      <div style="font-size: 1.3rem; font-weight: 700; color: #F1F5F9; letter-spacing: -0.02em;">
        🛡️ SecureIjazah
      </div>
      <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.2rem;">
        Sistem Keamanan Dokumen
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.75rem;">
      Teknologi
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1E293B; border-radius:10px; padding:0.9rem 1rem; margin-bottom:0.6rem;">
      <div style="font-size:0.8rem; font-weight:600; color:#60A5FA;">🔐 AES-256</div>
      <div style="font-size:0.72rem; color:#94A3B8; margin-top:0.2rem;">Enkripsi Data Mahasiswa</div>
    </div>
    <div style="background:#1E293B; border-radius:10px; padding:0.9rem 1rem; margin-bottom:1.5rem;">
      <div style="font-size:0.8rem; font-weight:600; color:#34D399;">🖼️ LSB Steganography</div>
      <div style="font-size:0.72rem; color:#94A3B8; margin-top:0.2rem;">Penyisipan Data ke Gambar</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.75rem;">
      Panduan Penggunaan
    </div>
    <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.7;">
      <b style="color:#CBD5E1;">Tab Pengamanan</b><br>
      Untuk pihak kampus yang ingin menyematkan data mahasiswa ke dalam foto ijazah.<br><br>
      <b style="color:#CBD5E1;">Tab Verifikasi</b><br>
      Untuk pihak HRD atau instansi untuk membuktikan keaslian ijazah.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.72rem; color: #475569;">
      © 2026 — Tugas Besar Kriptografi
    </div>
    """, unsafe_allow_html=True)

col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown("""
    <div style="padding: 0.5rem 0 0.25rem 0;">
      <h1 style="font-size:1.8rem; font-weight:700; color:#0F172A; margin:0; letter-spacing:-0.02em;">
        Sistem Keamanan & Verifikasi Ijazah
      </h1>
      <p style="font-size:0.9rem; color:#64748B; margin: 0.4rem 0 0 0;">
        Platform pengamanan dokumen akademik terintegrasi menggunakan <strong>Kriptografi AES-256</strong> dan <strong>Steganografi LSB</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style="display:flex; justify-content:flex-end; gap:0.5rem; padding-top:0.5rem;">
      <span class="badge">AES-256</span>
      <span class="badge badge-green">LSB Steganography</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 1rem 0 1.5rem 0;'>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  🔒  Pengamanan  ", "  🔍  Verifikasi  "])

with tab1:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <h3 style="font-size:1.1rem; font-weight:600; color:#0F172A; margin:0 0 0.3rem 0;">
        Pengamanan Data Mahasiswa
      </h3>
      <p style="font-size:0.875rem; color:#64748B; margin:0;">
        Lengkapi formulir, unggah foto, dan sistem akan secara otomatis mengenkripsi serta menyisipkan data ke dalam gambar.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_pengamanan"):
        st.markdown("""
        <p style="font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                  color:#94A3B8; margin-bottom:1rem;">
          Data Mahasiswa
        </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            nim  = st.text_input("NIM")
            ipk  = st.text_input("IPK")
        with col2:
            nama  = st.text_input("Nama Lengkap")
            lulus = st.text_input("Tahun Lulus")

        st.markdown("<hr style='border:none;border-top:1px solid #1E293B;margin:1.5rem 0;'>", unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                  color:#94A3B8; margin-bottom:1rem;">
          Keamanan & Gambar
        </p>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            password_encode = st.text_input(
                "Password Rahasia (AES Key)",
                type="password",
                key="pass_enc",
                placeholder="Minimal 8 karakter",
                help="Gunakan password yang kuat. Password ini dibutuhkan saat verifikasi."
            )
        with col4:
            uploaded_file = st.file_uploader(
                "Unggah Foto Ijazah(PNG / JPG)",
                type=["png", "jpg", "jpeg"],
                key="file_enc",
                help="Gunakan gambar PNG lossless untuk hasil terbaik."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("  🚀  Proses Pengamanan Data  ", type="primary")

        if submitted:
            if nim and nama and ipk and lulus and password_encode and uploaded_file:
                with st.spinner("Mengenkripsi data dan menyisipkan ke gambar..."):
                    data_asli = f"NIM: {nim} | Nama: {nama} | IPK: {ipk} | Lulus: {lulus}"
                    ciphertext = kripto_aes.encrypt_aes(data_asli, password_encode)

                    if "Error" not in ciphertext:
                        temp_input_path  = "temp_input.png"
                        temp_output_path = "stego_result.png"
                        img = Image.open(uploaded_file)
                        img.save(temp_input_path)
                        hasil_stego = stego_lsb.hide_data_lsb(temp_input_path, ciphertext, temp_output_path)

                        if "Sukses" in hasil_stego:
                            st.success("✅  Data berhasil dienkripsi dan disisipkan ke dalam foto.")
                            st.markdown("<br>", unsafe_allow_html=True)
                            r1, r2 = st.columns([1, 2])
                            with r1:
                                st.image(temp_output_path, caption=f"Stego-image — {nama}", use_container_width=True)
                            with r2:
                                st.markdown(f"""
                                <div class="section-card" style="height:100%;">
                                  <p style="font-size:0.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#64748B;">Ringkasan</p>
                                  <table style="width:100%;font-size:0.875rem;border-collapse:collapse;">
                                    <tr><td style="padding:.4rem 0;color:#94A3B8;width:40%">NIM</td><td style="color:#0F172A;font-weight:600">{nim}</td></tr>
                                    <tr><td style="padding:.4rem 0;color:#94A3B8">Nama</td><td style="color:#0F172A;font-weight:600">{nama}</td></tr>
                                    <tr><td style="padding:.4rem 0;color:#94A3B8">IPK</td><td style="color:#0F172A;font-weight:600">{ipk}</td></tr>
                                    <tr><td style="padding:.4rem 0;color:#94A3B8">Lulus</td><td style="color:#0F172A;font-weight:600">{lulus}</td></tr>
                                  </table>
                                </div>
                                """, unsafe_allow_html=True)
                                with open(temp_output_path, "rb") as file:
                                    st.download_button(
                                        label="  💾  Unduh Foto Aman (Stego-image)  ",
                                        data=file,
                                        file_name=f"SecurePhoto_{nim}.png",
                                        mime="image/png"
                                    )
                        else:
                            st.error(f"❌  {hasil_stego}")
                    else:
                        st.error("❌  Gagal melakukan enkripsi AES.")
            else:
                st.warning("⚠️  Mohon lengkapi semua kolom, masukkan password, dan unggah foto.")

with tab2:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <h3 style="font-size:1.1rem; font-weight:600; color:#0F172A; margin:0 0 0.3rem 0;">
        Verifikasi Keaslian Ijazah
      </h3>
      <p style="font-size:0.875rem; color:#64748B; margin:0;">
        Unggah pas foto yang terdapat pada ijazah, kemudian masukkan password verifikasi untuk membuktikan keaslian dokumen.
      </p>
    </div>
    """, unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([1, 1.4])

    with v_col1:
        st.markdown("""
        <p style="font-size:0.75rem; font-weight:600; color:#374151; margin-bottom:0.5rem;">
          Unggah Pas Foto dari Ijazah
        </p>
        """, unsafe_allow_html=True)
        uploaded_stego = st.file_uploader(
            "Format PNG",
            type=["png"],
            key="file_dec",
            label_visibility="collapsed"
        )
        if uploaded_stego:
            st.image(uploaded_stego, caption="Foto yang akan diverifikasi", use_container_width=True)

    with v_col2:
        st.markdown("""
        <p style="font-size:0.75rem; font-weight:600; color:#374151; margin-bottom:0.5rem;">
          Password Verifikasi
        </p>
        """, unsafe_allow_html=True)
        password_decode = st.text_input(
            "Password",
            type="password",
            key="pass_dec",
            placeholder="Masukkan password yang digunakan saat pengamanan",
            label_visibility="collapsed",
            help="Password ini harus sama dengan yang digunakan pihak kampus saat proses pengamanan."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        verify_btn = st.button("  🛡️  Verifikasi Dokumen  ", type="primary", key="verify_btn")

        if verify_btn:
            if uploaded_stego and password_decode:
                with st.spinner("Mengekstrak dan mendekripsi data..."):
                    temp_stego_path = "temp_stego_verify.png"
                    img = Image.open(uploaded_stego)
                    img.save(temp_stego_path)

                    extracted_ciphertext = stego_lsb.extract_data_lsb(temp_stego_path)

                    if "Gagal" not in extracted_ciphertext:
                        plaintext = kripto_aes.decrypt_aes(extracted_ciphertext, password_decode)

                        if "ERROR" not in plaintext:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("""
                            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px;
                                        padding:1rem 1.5rem; display:flex; align-items:center; gap:0.75rem; margin-bottom:1.5rem;">
                              <span style="font-size:1.5rem;">✅</span>
                              <div>
                                <div style="font-weight:700; color:#065F46; font-size:0.95rem;">Verifikasi Berhasil — Dokumen Asli</div>
                                <div style="font-size:0.8rem; color:#047857;">Data berhasil diekstrak dan didekripsi dari gambar.</div>
                              </div>
                            </div>
                            """, unsafe_allow_html=True)

                            res1, res2 = st.columns([1, 1.6])

                            with res1:
                                st.markdown("<p style='font-size:0.75rem;font-weight:600;color:#374151;margin-bottom:0.5rem;'>Tingkat Keaslian</p>", unsafe_allow_html=True)
                                chart_data = pd.DataFrame(
                                    {"Status": ["Asli (Verified)", "Palsu/Lainnya"], "Persentase": [100, 0]}
                                )
                                chart = alt.Chart(chart_data).mark_arc(innerRadius=55, outerRadius=85).encode(
                                    theta=alt.Theta(field="Persentase", type="quantitative"),
                                    color=alt.Color(
                                        field="Status", type="nominal",
                                        scale=alt.Scale(domain=["Asli (Verified)", "Palsu/Lainnya"], range=["#10B981", "#E2E8F0"]),
                                        legend=alt.Legend(orient="bottom", title=None, labelFontSize=11)
                                    ),
                                    tooltip=["Status", "Persentase"]
                                ).properties(height=230)
                                st.altair_chart(chart, use_container_width=True)

                            with res2:
                                st.markdown("<p style='font-size:0.75rem;font-weight:600;color:#374151;margin-bottom:0.75rem;'>Data Mahasiswa yang Ditemukan</p>", unsafe_allow_html=True)
                                data_dict = {"Kategori": [], "Data": []}
                                for item in plaintext.split("|"):
                                    if ":" in item:
                                        key, val = item.split(":", 1)
                                        data_dict["Kategori"].append(key.strip())
                                        data_dict["Data"].append(val.strip())
                                df = pd.DataFrame(data_dict)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.markdown("""
                            <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px;
                                        padding:1rem 1.5rem; display:flex; align-items:center; gap:0.75rem; margin-top:1rem;">
                              <span style="font-size:1.5rem;">❌</span>
                              <div>
                                <div style="font-weight:700; color:#991B1B; font-size:0.95rem;">Verifikasi Gagal</div>
                                <div style="font-size:0.8rem; color:#B91C1C;">Password salah atau foto telah dipalsukan/dimodifikasi.</div>
                              </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px;
                                    padding:1rem 1.5rem; display:flex; align-items:center; gap:0.75rem; margin-top:1rem;">
                          <span style="font-size:1.5rem;">🚫</span>
                          <div>
                            <div style="font-weight:700; color:#991B1B; font-size:0.95rem;">Data Tidak Ditemukan</div>
                            <div style="font-size:0.8rem; color:#B91C1C;">Tidak ada data rahasia pada foto ini. Kemungkinan besar palsu atau belum diamankan.</div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️  Mohon unggah foto dan masukkan password verifikasi.")