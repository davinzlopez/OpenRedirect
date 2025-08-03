# OpenRedirect
Scanner untuk menguji kerentanan Open Redirect pada URL dengan berbagai parameter umum dan payload bypass.
# 🔍 Open Redirect Scanner

Open Redirect Scanner adalah tool sederhana berbasis Python yang digunakan untuk menguji kerentanan **Open Redirect** pada satu atau banyak URL target. Alat ini menguji berbagai parameter umum dan payload bypass untuk mendeteksi redirect tidak sah.

## 🧠 Fitur

- Memindai satu URL atau banyak URL dari file `.txt`
- Menggunakan berbagai parameter redirect umum
- Payload bypass untuk menghindari filter sederhana
- Tidak mengikuti redirect (menggunakan `allow_redirects=False`)
- Mendukung payload yang telah di-encode

## 🚀 Instalasi

1. **Clone repositori ini**
   ```
   git clone https://github.com/davinzlopez/OpenRedirect.git
   cd open-redirect-scanner
2.**Install dependencies**
  ```
pip install -r requirements.txt

🛠️ Cara Penggunaan
Mode 1: Uji satu URL
python open_redirect_scanner.py
Pilih opsi [1], lalu masukkan URL target, misalnya:
https://example.com/redirect

Mode 2: Uji banyak URL dari file .txt
Siapkan file berisi daftar URL (satu URL per baris), misalnya:
urls.txt
Lalu jalankan:
python open_redirect.py
Pilih opsi [2], lalu masukkan path file:
urls.txt

🧪 Contoh Output
[✅] https://example.com/redirect?url=https%3A%2F%2Fbing.com -> ://bing.com (Status: 302)
