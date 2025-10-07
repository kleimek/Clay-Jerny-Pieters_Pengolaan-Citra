import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

# ========== STYLE GLOBAL ==========
st.set_page_config(page_title="✨ PixelScope - RGB Scanner", layout="centered")

st.markdown("""
<style>
/* === Background putih === */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-family: 'Segoe UI', sans-serif !important;
}

/* === Kontainer utama (gelap) === */
.main > div {
    background: #1a1a1a !important;
    border-radius: 20px !important;
    padding: 1.8rem 2.2rem !important;
    border: 1px solid rgba(0, 0, 0, 0.15) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    color: #FFFFFF !important;
}

/* === Teks utama (hitam di background putih) === */
h1, h2, h3, h4, p, label, span, div, .stMarkdown {
    color: #000000 !important;
}

/* === Box warna pixel === */
.pixel-box {
    width: 80px; height: 80px;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

/* === File uploader === */
div[data-testid="stFileUploader"] > section {
    border: 2px dashed rgba(0,0,0,0.4) !important;
    border-radius: 15px !important;
    background-color: #2a2a2a !important;
    color: #FFFFFF !important;
}
div[data-testid="stFileUploader"] * {
    color: #FFFFFF !important;
}
div[data-testid="stFileUploader"] > section:hover {
    background-color: #3a3a3a !important;
}

/* === Tombol "Browse files" === */
div[data-testid="stFileUploader"] button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
div[data-testid="stFileUploader"] button:hover {
    background-color: #e6e6e6 !important;
}

/* === Tabel === */
.stDataFrame {
    border-radius: 12px !important;
    background-color: #2a2a2a !important;
    color: #FFFFFF !important;
}

/* === Divider & Footer === */
hr {
    border: none !important;
    border-top: 1px solid rgba(0,0,0,0.2) !important;
}
footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("<h1 style='text-align:center;'>✨ PixelScope</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Deteksi warna piksel dengan tema gelap di atas latar putih</p>", unsafe_allow_html=True)

# ========== UPLOADER ==========
uploaded_file = st.file_uploader("📤 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    height, width = img_array.shape[:2]

    st.markdown(f"<h4>📏 Ukuran gambar:</h4> <p><b>{width} × {height}</b> px</p>", unsafe_allow_html=True)

    # TABEL PIXEL
    pixels = [[f"({r},{g},{b})" for (r, g, b) in row] for row in img_array[:, :, :3]]
    df_full = pd.DataFrame(pixels)

    with st.expander("📋 Lihat seluruh tabel pixel", expanded=False):
        st.dataframe(df_full, use_container_width=True)

    # GAMBAR INTERAKTIF
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

            # Area sekitar (5×5)
            st.markdown("### 🟦 Area sekitar (5×5 pixel):")
            y_start, y_end = max(0, y-2), min(height, y+3)
            x_start, x_end = max(0, x-2), min(width, x+3)
            neighborhood = df_full.iloc[y_start:y_end, x_start:x_end]
            st.dataframe(neighborhood, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>🌌 Dibuat dengan gaya gelap modern — by Gibran 🌌</p>", unsafe_allow_html=True)

else:
    st.info("📁 Silakan upload gambar terlebih dahulu.")
