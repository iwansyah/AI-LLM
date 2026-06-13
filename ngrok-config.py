from pyngrok import ngrok
from google.colab import userdata

# Ambil token dari Colab Secrets
ngrok.set_auth_token(userdata.get('NGROK_TOKEN'))
print("ngrok token berhasil dikonfigurasi!")
