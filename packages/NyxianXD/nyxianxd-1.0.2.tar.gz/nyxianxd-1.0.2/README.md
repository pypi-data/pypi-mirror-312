# NyxianXD
NyxianXD adalah pustaka Python untuk berinteraksi dengan endpoint uploader Nyxian tanpa perlu mengungkapkan URL endpoint.

## Instalasi
```
pip install NyxianXD
```

## Contoh Penggunaan
```python
from NyxianXD import NyxianXD

# Inisialisasi dengan API Key Anda
client = NyxianXD("API_KEY_ANDA")

# Mendapatkan informasi pengguna
user_info = client.get_user_info()
print(user_info)

# Mengunggah file
url = client.upload_file("path/to/your/file.jpg")
print("File URL:", url)
```
