import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="🎨 PixelScope", layout="centered")

st.markdown("""
<style>
/* Background global putih */
html, body, [class*="stAppViewContainer"], [class*="stMainBlockContainer"] {
    background-color: #ffffff !important;
    color: #ffffff;
    font-family: "Inter", "Segoe UI", sans-serif;
}

/* Box utama (kontainer isi) berwarna gelap */
.main > div {
    background-color: #1f2937 !important;  /* abu gelap */
    color: #f9fafb !important;  /* teks putih terang */
    border-radius: 16px;
    padding: 1.8rem 2rem;
    border: 1px solid #374151;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

/* Judul dan heading di dalam box */
h1, h2, h3, h4 {
    color: #f9fafb !important;
}
.stMarkdown, p, label {
    color: #e5e7eb !important;
}

/* Kotak warna piksel (pixel-box) */
.pixel-box {
    width: 80px; height: 80px;
    border-radius: 12px;
    border: 2px solid #4b5563;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

/* Uploader — jangan gelap, gunakan tema terang agar tombol “Browse” jelas */
div[data-testid="stFileUploader"] > section {
    background-color: #f9fafb !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 10px;
    color: #374151 !important;
    transition: background-color 0.2s ease;
}
div[data-testid="stFileUploader"] > section:hover {
    background-color: #f1f5f9 !important;
}

/* Tabel / DataFrame dalam box gelap */
.stDataFrame {
    border-radius: 10px !important;
    background-color: #111827 !important;
    color: #f9fafb !important;
}

/* Garis horizontal */
hr {
    border: none;
    border-top: 1px solid #374151;
}

/* Sembunyikan footer Streamlit default */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("<h1 style='text-align:center;'>🎨 PixelScope</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#d1d5db;'>Analisis warna piksel — Tema gelap dalam box</p>", unsafe_allow_html=True)

# ========== UPLOADER ==========
uploaded_file = st.file_uploader("📤 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    height, width = img_array.shape[:2]

    st.markdown(f"<h4>📏 Ukuran gambar:</h4> <p><b>{width} × {height}</b> px</p>", unsafe_allow_html=True)

    # ====== TABEL PIXEL ======
    pixels = [[f"({r},{g},{b})" for (r, g, b) in row] for row in img_array[:, :, :3]]
    df_full = pd.DataFrame(pixels)

    with st.expander("📋 Lihat seluruh tabel pixel", expanded=False):
        st.dataframe(df_full, use_container_width=True)

    # ====== GAMBAR INTERAKTIF ======
    st.markdown("### 🖱️ Klik gambar untuk deteksi warna:")
    coords = streamlit_image_coordinates(image)

    if coords is not None:
        x, y = coords["x"], coords["y"]
        st.success(f"📍 Koordinat dipilih: (x={x}, y={y})")

        if y < img_array.shape[0] and x < img_array.shape[1]:
            r, g, b = img_array[y, x][:3]
            hex_color = '#%02x%02x%02x' % (r, g, b)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div class='pixel-box' style='background-color:rgb({r},{g},{b});'></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h4>🎨 RGB:</h4> <p><b>({r}, {g}, {b})</b></p>", unsafe_allow_html=True)
                st.markdown(f"<h4>💠 HEX:</h4> <p><b>{hex_color.upper()}</b></p>", unsafe_allow_html=True)

            # Baris pixel
            st.markdown(f"### 🔎 Baris ke-{y}")
            row_focus = pd.DataFrame([df_full.iloc[y]], index=[f"Row {y}"])
            st.dataframe(row_focus, use_container_width=True)

            # Area sekitar 5×5
            st.markdown("### 🟩 Area sekitar (5×5 pixel):")
            y_start, y_end = max(0, y-2), min(height, y+3)
            x_start, x_end = max(0, x-2), min(width, x+3)
            neighborhood = df_full.iloc[y_start:y_end, x_start:x_end]
            st.dataframe(neighborhood, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#d1d5db;'>🔍 Dibuat dengan kesederhanaan — by Gibran</p>", unsafe_allow_html=True)

else:
    st.info("📁 Silakan upload gambar terlebih dahulu.")
