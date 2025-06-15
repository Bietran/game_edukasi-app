# main.py - Game Edukasi Pemilahan Sampah (Versi Final - Quiz Berjalan)
import streamlit as st
import random
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
import os
import base64
import time

st.set_page_config(page_title="Game Pemilahan Sampah", layout="centered")

# === FUNGSI SUARA === #
def play_local_sound(sound_file_path):
    if os.path.exists(sound_file_path):
        with open(sound_file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)


# === TRAIN MODEL SECARA LANGSUNG === #
@st.cache_resource
def train_model():
    # Contoh sederhana pakai dataset iris
    data = load_iris()
    X, y = data.data, data.target
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)
    return model

model = train_model()


# Soal mini quiz
quiz_questions = [
    {
        "question": "Apa yang harus dilakukan sebelum membuang sampah?",
        "options": ["Dibiarkan berserakan", "Dipilah sesuai jenisnya", "Dibakar di halaman", "Dimasukkan semua ke satu kantong"],
        "answer": 1
    },
    {
        "question": "Mana yang termasuk sampah organik?",
        "options": ["Botol plastik", "Kaleng bekas", "Daun kering", "Kertas koran"],
        "answer": 2
    },
    {
        "question": "Sampah apa yang tidak boleh dibuang sembarangan karena beracun?",
        "options": ["Kulit buah", "Daun kering", "Baterai bekas", "Kertas"],
        "answer": 2
    },
    {
        "question": "Apakah botol plastik termasuk sampah anorganik?",
        "options": ["Ya", "Tidak"],
        "answer": 0
    },
    {
        "question": "Apa yang terjadi jika sampah tidak dipilah?",
        "options": ["Lebih mudah didaur ulang", "Meningkatkan limbah", "Tidak ada efek", "Semua benar"],
        "answer": 1
    }
]

# Gambar sampah dengan nama
image_files = {
    "Organik": [
        {"name": "Daun", "file": "daun.jpeg"},
        {"name": "Kulit Pisang", "file": "kulit_pisang.jpeg"},
        {"name": "Daun Kering", "file": "daun_kering.jpeg"},
        {"name": "Sisa Makanan", "file": "sisa_makanan.jpeg"},
        {"name": "Buah Busuk", "file": "buah_busuk.jpeg"}
    ],
    "Anorganik": [
        {"name": "Botol Plastik", "file": "botol_plastik.jpeg"},
        {"name": "Kaleng", "file": "kaleng.jpeg"},
        {"name": "Kemasan Snack", "file": "kemasan_snack.jpeg"},
        {"name": "Tutup Botol", "file": "tutup_botol.jpeg"},
        {"name": "Sedotan", "file": "sedotan.jpeg"}
    ]
}

# Inisialisasi session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = ""
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = ""
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'show_quiz' not in st.session_state:
    st.session_state.show_quiz = False
if 'quiz_done' not in st.session_state:
    st.session_state.quiz_done = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'play_sound' not in st.session_state:
    st.session_state.play_sound = None
if 'show_final_summary' not in st.session_state:
    st.session_state.show_final_summary = False
if 'used_images' not in st.session_state:
    st.session_state.used_images = []
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'selected_image_data' not in st.session_state:
    st.session_state.selected_image_data = None
if 'quiz_used' not in st.session_state:
    st.session_state.quiz_used = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

# UI
st.title("♻️ Game Edukasi Pemilahan Sampah")
st.subheader("Ayo belajar mengelola sampah dengan benar!")

# Tombol mulai
if not st.session_state.game_started:
    st.title("\U0001F4AA Game Edukasi Pemilahan Sampah")
    st.subheader("Belajar membuang sampah dengan benar yuk!")
    st.image("images/tampilan.png", use_container_width=True)

    # === Tutorial Bermain ===
    with st.expander("📖 Cara Bermain (Klik untuk melihat)"):
        st.markdown("""
        🧒 **Hai teman-teman! Yuk belajar membuang sampah dengan benar!**

        👇 Berikut cara bermain game ini:

        1️⃣ Akan muncul gambar **sampah** di layar.

        2️⃣ Bacalah **nama sampahnya**, lalu **klik tombol** sesuai jenisnya:
        - 🟢 **Organik** untuk sampah dari alam (daun, kulit buah, sisa makanan).
        - 🔴 **Anorganik** untuk sampah buatan (botol, plastik, kaleng).

        3️⃣ Jika benar, kamu akan dapat suara senang dan poin ⭐

        4️⃣ Setelah beberapa soal, akan ada **Mini Quiz** untuk menguji pengetahuanmu!

        ✨ Ayo kumpulkan skor setinggi-tingginya dan jadi pahlawan lingkungan!
        """)

        # Opsional: Tambahkan audio petunjuk jika ada
        if os.path.exists("audio/tutorial.mp3"):
            st.audio("audio/tutorial.mp3", format="audio/mp3", autoplay=False)

    st.write("Tekan tombol di bawah untuk memulai permainan:")
    if st.button("🎮 Mulai Game", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.name = "Anak Cerdas"
        st.session_state.used_images = []
        st.session_state.question_count = 0
        st.session_state.score = 0
        st.rerun()
else:
    st.markdown(f"### Halo, {st.session_state.name}!")
    st.markdown(f"#### Skor kamu saat ini: **{st.session_state.score}**")

    if st.session_state.last_result:
        if st.session_state.last_result == "benar":
            st.success("✅ Jawaban benar!")
        else:
            st.error("❌ Jawaban salah!")
        play_local_sound(st.session_state.play_sound)
        st.session_state.last_result = None
        st.session_state.play_sound = None
        time.sleep(2)
        st.rerun()

    elif st.session_state.show_final_summary:
        st.markdown("### 🎉 Selamat! Kamu telah menyelesaikan permainan.")
        st.markdown(f"#### Total Skor Akhir: **{st.session_state.score}**")

        if st.session_state.score >= 50:
            st.balloons()
            st.success("🌟 Wah, kamu sangat hebat memilah sampah!")
        elif st.session_state.score >= 20:
            st.info("👍 Bagus! Terus belajar ya.")
        else:
            st.warning("🌱 Ayo coba lagi dan tingkatkan skormu!")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Ulangi Lagi", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        with col2:
            if st.button("🚪 Keluar", use_container_width=True):
                st.success("🎮 Terima kasih telah bermain. Sampai jumpa!")
                st.stop()

    elif st.session_state.show_quiz:
        all_questions = quiz_questions.copy()
        total_soal = len(all_questions)

        if st.session_state.quiz_index >= len(all_questions):
            st.markdown("### 🎉 Kamu telah menyelesaikan mini quiz!")
            st.markdown(f"#### Skor Quiz: **{st.session_state.quiz_score} / {total_soal * 10}**")

            if st.session_state.quiz_score >= 30:
                st.balloons()
                st.success("🎉 Hebat! Kamu lulus mini quiz.")
            elif st.session_state.quiz_score >= 10:
                st.info("👍 Lumayan, coba lagi untuk skor sempurna.")
            else:
                st.warning("🌱 Ayo belajar lagi dan tingkatkan skormu!")

            if st.button("🔁 Main Lagi", use_container_width=True):
                st.session_state.clear()
                st.rerun()

            if st.button("🚪 Keluar", use_container_width=True):
                st.success("🎮 Terima kasih telah bermain. Sampai jumpa!")
                st.stop()

        else:
            idx = st.session_state.quiz_index
            q = all_questions[idx]
            st.write("### 🧠 Pertanyaan Mini Quiz")
            st.write(f"**Soal {idx + 1} dari {total_soal}**")
            st.write(q["question"])
            selected = st.radio("Pilih jawaban:", q["options"], key=f"quiz_{idx}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Cek Jawaban", use_container_width=True):
                    if q["options"].index(selected) == q["answer"]:
                        st.session_state.quiz_score += 20
                        st.session_state.score += 20
                        st.session_state.last_result = "benar"
                        st.session_state.play_sound = "audio/benar.mp3"
                    else:
                        st.session_state.last_result = "salah"
                        st.session_state.play_sound = "audio/salah.mp3"

                    st.session_state.quiz_index += 1
                    time.sleep(1)
                    st.rerun()

            with col2:
                if st.button("🔚 Kembali", use_container_width=True):
                    st.session_state.show_quiz = False
                    st.rerun()

    else:
        if not st.session_state.current_image:
            # Batasi hingga 10 pertanyaan
            if st.session_state.question_count >= 10:
                st.session_state.show_final_summary = True
                st.rerun()

            category = random.choice(["Organik", "Anorganik"])
            available_images = [img for img in image_files[category] if img["file"] not in st.session_state.used_images]
            if not available_images:
                st.error("⚠️ Semua gambar sudah digunakan. Silakan mulai ulang.")
                st.session_state.show_final_summary = True
                st.rerun()

            selected_image = random.choice(available_images)
            st.session_state.current_image = os.path.join("images", selected_image["file"])
            st.session_state.correct_answer = category
            st.session_state.used_images.append(selected_image["file"])
            st.session_state.question_count += 1
            st.session_state.selected_image_data = selected_image
            st.rerun()

        # Tampilkan gambar dan nama
        st.image(st.session_state.current_image, width=250)
        st.markdown(f"### 📝 Nama: **{st.session_state.selected_image_data['name']}**")

        st.markdown("### 🗑️ Buang ke jenis sampah yang benar:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟢 Organik", use_container_width=True):
                user_choice = "Organik"
                if user_choice == st.session_state.correct_answer:
                    st.session_state.score += 10
                    st.session_state.last_result = "benar"
                    st.session_state.play_sound = "audio/benar.mp3"
                else:
                    st.session_state.last_result = "salah"
                    st.session_state.play_sound = "audio/salah.mp3"
                st.session_state.current_image = ""
                st.rerun()

        with col2:
            if st.button("🔴 Anorganik", use_container_width=True):
                user_choice = "Anorganik"
                if user_choice == st.session_state.correct_answer:
                    st.session_state.score += 10
                    st.session_state.last_result = "benar"
                    st.session_state.play_sound = "audio/benar.mp3"
                else:
                    st.session_state.last_result = "salah"
                    st.session_state.play_sound = "audio/salah.mp3"
                st.session_state.current_image = ""
                st.rerun()

        if st.button("🔚 Selesai Bermain", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# Tombol akses quiz
if st.button("🎯 Ambil Quiz", use_container_width=True):
    st.session_state.show_quiz = True
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_used = []
    st.rerun()
