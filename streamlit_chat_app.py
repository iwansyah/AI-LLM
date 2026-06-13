%%writefile streamlit_chat_app.py
# Import library yang dibutuhkan
import streamlit as st          # framework web app
from google import genai         # SDK Gemini dari Google
from google.genai import types   # Untuk mengatur instruksi sistem/persona

# ── 1. Konfigurasi Halaman & Tema Warna (Merah Putih) ────────────────────────
st.set_page_config(page_title="AI CS IPstore", page_icon="🎧")

# Injeksi CSS untuk Sidebar Merah dan Layar Utama Putih
st.markdown("""
    <style>
        /* 1. Layar Utama dan Header tetap PUTIH */
        [data-testid="stAppViewContainer"], 
        [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }

        /* 2. Mengubah background SIDEBAR menjadi MERAH secara paksa */
        [data-testid="stSidebar"] {
            background-color: #E60000 !important;
        }
        /* Streamlit kadang menaruh warna latar di elemen anak sidebar */
        [data-testid="stSidebar"] > div:first-child {
            background-color: #E60000 !important;
        }

        /* 3. Mengubah teks khusus di dalam SIDEBAR menjadi PUTIH agar terbaca jelas */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }

        /* 4. Teks di Layar Utama tetap GELAP/HITAM */
        [data-testid="stAppViewContainer"] p, 
        [data-testid="stAppViewContainer"] span {
            color: #262730 !important;
        }
        /* Judul utama AI CS IPstore tetap Merah */
        [data-testid="stAppViewContainer"] h1 {
            color: #E60000 !important;
        }

        /* 5. Tombol Reset di Sidebar (Background Putih, Teks Merah) agar kontras */
        [data-testid="baseButton-primary"] {
            background-color: #FFFFFF !important;
            border-color: #FFFFFF !important;
        }
        [data-testid="baseButton-primary"] p {
            color: #E60000 !important;
            font-weight: 600 !important;
        }
        [data-testid="baseButton-primary"]:hover {
            background-color: #F0F0F0 !important;
            border-color: #F0F0F0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Menampilkan judul dan keterangan di bagian atas
st.title("AI CS IPstore 🎧")
st.caption("Layanan bantuan pelanggan seputar informasi, spesifikasi, dan fitur produk iPhone.")

# ── 2. Sidebar: Pengaturan App ───────────────────────────────────────────────
with st.sidebar:
    st.subheader("Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("Reset Percakapan", help="Hapus semua pesan dan mulai dari awal")

# ── 3. Validasi API Key ──────────────────────────────────────────────────────
if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk mulai chat.", icon="🗝️")
    st.stop()

# ── 4. Inisialisasi Gemini Client ────────────────────────────────────────────
if ("genai_client" not in st.session_state) or (
    getattr(st.session_state, "_last_key", None) != google_api_key
):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key

        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)

    except Exception as e:
        st.error(f"API Key tidak valid: {e}")
        st.stop()

# ── 5. Inisialisasi Chat Session & Riwayat Pesan ────────────────────────────
if "chat" not in st.session_state:
    # Menambahkan SYSTEM INSTRUCTION sebagai Customer Support AI CS IPstore
    cs_instruction = """
    Kamu adalah Customer Support AI dari IPstore, spesialis produk Apple khususnya iPhone. 
    Tugas utamamu adalah membantu pelanggan dengan ramah, sopan, dan profesional.
    Fokuskan jawabanmu pada informasi produk iPhone, perbandingan spesifikasi antar model, fitur-fitur iOS, informasi garansi, serta panduan mengatasi masalah teknis dasar pada iPhone.
    Jika ada pertanyaan di luar produk Apple atau iPhone, arahkan kembali pembicaraan ke topik iPhone dengan sopan.
    Gunakan bahasa Indonesia yang baik, mudah dipahami, dan selalu tawarkan bantuan lebih lanjut di akhir kalimat.
    """
    
    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=cs_instruction,
            temperature=0.3 # Diperkecil agar jawaban spesifikasi akurat
        )
    )

if "messages" not in st.session_state:
    # Pesan sambutan otomatis
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Selamat datang di layanan pelanggan AI CS IPstore. Ada pertanyaan seputar iPhone atau fitur iOS yang bisa saya bantu hari ini?"}
    ]

# ── 6. Tombol Reset ──────────────────────────────────────────────────────────
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ── 7. Tampilkan Riwayat Percakapan ─────────────────────────────────────────
for msg in st.session_state.messages:
    avatar_icon = "🎧" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# ── 8. Input & Respons ───────────────────────────────────────────────────────
prompt = st.chat_input("Ketik pertanyaan mengenai iPhone di sini...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        
        if hasattr(response, "text"):
            answer = response.text
        else:
            answer = str(response)

    except Exception as e:
        answer = f"Terjadi error: {e}"

    with st.chat_message("assistant", avatar="🎧"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
