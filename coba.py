import streamlit as st
import base64
import os

# Fungsi untuk memainkan file mp3 lokal menggunakan base64 encoding
def play_local_sound(sound_file_path):
    with open(sound_file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# Judul dan instruksi
st.title("🎮 Game Edukasi Sampah")
st.write("Pilih jenis sampah yang benar untuk soal berikut:")

# Contoh soal
soal = "Sisa makanan termasuk jenis sampah?"
pilihan = st.radio(soal, ["Organik", "Anorganik", "B3"])
jawaban_benar = "Organik"

# Saat tombol diklik
if st.button("Jawab"):
    if pilihan == jawaban_benar:
        st.success("✅ Jawaban Benar!")
        play_local_sound("audio/benar.mp3")
    else:
        st.error("❌ Jawaban Salah!")
        play_local_sound("audio/salah.mp3")
