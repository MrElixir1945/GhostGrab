# 👻 GhostGrab — Social Media Video Downloader Bot

> Telegram bot untuk download video dari TikTok, Instagram, Twitter/X, dan YouTube — tanpa watermark, langsung di chat.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22.6-blue) ![yt-dlp](https://img.shields.io/badge/yt--dlp-2026.2.4-red) ![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?logo=linux) ![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Fitur

- 🎬 Download video dari **TikTok, Instagram, Twitter/X, YouTube**
- 🚫 Hapus watermark otomatis (jika platform mendukung)
- ⚡ Prioritas format **MP4 terbaik** via `yt-dlp`
- 📏 Validasi ukuran file otomatis (max **50 MB** sesuai batas Telegram Bot API)
- 🧹 **Auto-cleanup** — file di server langsung dihapus setelah terkirim
- ❌ Error handling: private video, age-restricted, video dihapus

---

## 🛠️ Tech Stack

| Komponen | Detail |
|---|---|
| Bahasa | Python 3 |
| Bot Framework | `python-telegram-bot` v22.6 |
| Download Engine | `yt-dlp` v2026.2.4 |
| Environment | Linux Ubuntu (LXC Container di Proxmox VE) |

---

## 🚀 Cara Deploy

### 1. Clone repo ini
```bash
git clone https://github.com/MrElixir1945/GhostGrab.git
cd GhostGrab
```

### 2. Buat virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi token
Buka `sosmed_bot.py`, cari baris berikut dan ganti dengan token bot kamu:
```python
TOKEN = "GANTI_DENGAN_TOKEN_BOT_KAMU"
```

> 💡 Atau gunakan `.env` + `python-dotenv` untuk pengelolaan token yang lebih aman.

### 5. Jalankan bot
```bash
python sosmed_bot.py
```

---

## 📁 Struktur Project

```
GhostGrab/
├── sosmed_bot.py       # Main bot
├── requirements.txt    # Dependencies
└── downloads/          # Folder temp (auto-dibuat, auto-dihapus setelah kirim)
```

---

## ⚙️ Cara Kerja

```
User kirim link
    ↓
Validasi URL (http/https)
    ↓
yt-dlp download video (format MP4 terbaik)
    ↓
Cek ukuran file (< 50 MB?)
    ↓ Ya                    ↓ Tidak
Upload ke Telegram      Batalkan + notifikasi user
    ↓
Hapus file dari server (cleanup)
```

---

## 📋 Contoh Penggunaan

```
User:  https://www.tiktok.com/@user/video/xxxxx
Bot:   ⏳ Sedang memproses...
Bot:   🚀 Mengupload ke Telegram...
Bot:   🎥 [Video terkirim dengan caption]
```

---

## ⚠️ Catatan

- Bot ini hanya untuk penggunaan **pribadi/edukasi**
- Hormati hak cipta konten yang kamu download
- Video **private** atau **age-restricted** tidak bisa didownload
- Batas ukuran 50 MB adalah ketentuan dari **Telegram Bot API**

---

## 👤 Author

**Mr. Elixir** — [@MrElixir1945](https://github.com/MrElixir1945)

*Self-hosted on Proxmox VE Home Server*

-Built with ❤️ and a bit of help from AI Gemini and Claude for logic optimization and debugging.