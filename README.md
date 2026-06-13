# AI-LLM
AI LLM - Streamlit for Chatbot

Installasi Guide :

Step 1 — Install Streamlit dan pyngrok

!pip install -q streamlit pyngrok google-genai

Step 2 — Daftarkan ngrok Auth Token

Cara mendapatkan token:

Daftar gratis di https://ngrok.com
Login → klik Your Authtoken di dashboard
Copy token-nya, paste ke Colab Secrets dengan nama NGROK_TOKEN (klik ikon 🔑 di sidebar kiri Colab)
Token ngrok gratis sudah cukup untuk keperluan training. Satu akun ngrok bisa membuka 1 tunnel aktif sekaligus.

Step 3 - Fungsi Helper: Jalankan Streamlit + Buka Tunnel
Kita buat fungsi reusable yang akan kita pakai berulang kali di setiap bagian. Fungsi ini melakukan tiga hal:

Menulis file .py ke disk
Menjalankan streamlit run di background
Membuka tunnel ngrok dan menampilkan URL publik
