import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- KONFIGURASI ---
TOKEN = "GANTI_DENGAN_TOKEN_BOT_KAMU"  # Ganti dengan token botmu
DOWNLOAD_DIR = "downloads"

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Pastikan folder download ada
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Halo!** Kirimkan link video (TikTok, IG, YouTube, Twitter).\n"
        "Saya akan downloadkan video **tanpa watermark** (jika bisa) untukmu.\n\n"
        "⚠️ *Batas ukuran: 50 MB (Aturan Telegram)*"
    , parse_mode='Markdown')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # Filter pesan yang bukan link (biar gak spam log)
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("Itu bukan link deh kayaknya. 😅")
        return

    msg = await update.message.reply_text("⏳ **Sedang memproses...**\n_Mencari metadata & download..._", parse_mode='Markdown')
    
    output_file = ""
    
    # Opsi yt-dlp (Kunci kesuksesan bot ini)
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s', # Format nama file
        'format': 'best[ext=mp4][filesize<50M]/best[ext=mp4]/best', # Prioritas: MP4 < 50MB
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True, # Biar nama file gak aneh-aneh
    }

    try:
        # Proses Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(info)

        # Cek Ukuran File sebelum Upload
        file_size = os.path.getsize(output_file)
        limit_mb = 49 * 1024 * 1024 # 49 MB biar aman

        if file_size > limit_mb:
            await msg.edit_text(f"❌ **Gagal Kirim.**\nVideonya kegedean ({file_size / (1024*1024):.2f} MB).\nTelegram cuma bolehin bot kirim max 50 MB.")
            os.remove(output_file) # Hapus file jumbo
            return

        # Upload ke Telegram
        await msg.edit_text("🚀 **Mengupload ke Telegram...**")
        
        # Kirim Video
        with open(output_file, 'rb') as video:
            # Ambil caption asli video (kalau ada), potong biar gak kepanjangan
            caption = info.get('title', 'Video Downloaded')[:100]
            await update.message.reply_video(
                video=video,
                caption=f"🎥 {caption}\n🤖 *Via Bot*",
                parse_mode='Markdown',
                supports_streaming=True
            )

        await msg.delete() # Hapus pesan "Processing..."

    except Exception as e:
        logging.error(f"Error: {e}")
        error_text = str(e)
        if "Sign in to confirm" in error_text:
            await msg.edit_text("🔒 **Gagal.** Video ini butuh login (Private/Age Restricted).")
        elif "Video unavailable" in error_text:
            await msg.edit_text("❌ **Gagal.** Video tidak ditemukan atau dihapus.")
        else:
            await msg.edit_text("❌ **Error.** Gagal mendownload link tersebut.")

    finally:
        # Cleanup: Hapus file setelah dikirim (SUKSES atau GAGAL wajib hapus)
        if output_file and os.path.exists(output_file):
            try:
                os.remove(output_file)
                logging.info(f"Deleted: {output_file}")
            except Exception as e:
                logging.error(f"Gagal hapus file: {e}")

if __name__ == '__main__':
    # Ganti token di sini juga kalau perlu, atau pakai variabel diatas
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # Handle pesan teks apapun yang mengandung http
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot Sosmed Downloader Berjalan...")
    app.run_polling()