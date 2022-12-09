import shutil
import time
from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
import logging
from HelperFunc.absolutePaths import absolutePaths
from HelperFunc.authUserCheck import AuthUserCheck
from HelperFunc.messageFunc import editMessage, sendMessage, sendMusic
from config import Config
import os
from pyrogram.errors import FloodWait

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from qobuz_dl.core import QobuzDL

qobuz = QobuzDL(directory="qobuzdown",quality=Config.QOBUZ_QUAL,embed_art=True,smart_discography=True) # kalite 6
qobuz.get_tokens() # get 'app_id' and 'secrets' attrs
qobuz.initialize_client(Config.QOBUZ_MAIL, Config.QOBUZ_PASS, qobuz.app_id, qobuz.secrets)

@Client.on_message(filters.command(["start", "q2"]))
def antiSpam(client: Client, message: Message):
    if not AuthUserCheck(message): return

    # tek işlem
    if os.path.isfile("calisiyor.txt"):
        a = sendMessage(message, f"Member Lain Sedang Mengunduh Lagu.\nTunggu Giliranmu {message.from_user.mention}\nJANGAN SPAM!!! ⛔️")
        time.sleep(15)
        return a.delete()
    else:
        with open("calisiyor.txt", "w") as f:
            f.write(".")
    # tek işlem

    linkler = []
    helpstr = f"""
Baca Pesan Tersemat Bro..!!

https://t.me/qobuzz/5683
"""
    if message.reply_to_message:
        if message.reply_to_message.document:
            try:
                inentxt = client.download_media(message.reply_to_message.document)
                with open(inentxt, encoding='utf8') as f:
                    linkler = f.read().split()
                os.remove(inentxt)
            except Exception as e:
                sendMessage(message, helpstr + "\n\n" + str(e))
                return os.remove("calisiyor.txt") if os.path.isfile("calisiyor.txt") else print("ok")
        elif message.reply_to_message.text:
            try: linkler = message.reply_to_message.text.split()
            except Exception as e:
                sendMessage(message, helpstr + "\n\n" + str(e))
                return os.remove("calisiyor.txt") if os.path.isfile("calisiyor.txt") else print("ok")
    else:
        try: linkler = message.text.split(" ", 1)[1].split()
        except Exception as e:
            sendMessage(message, helpstr + "\n\n" + str(e))
            return os.remove("calisiyor.txt") if os.path.isfile("calisiyor.txt") else print("ok")

    if linkler.count == 0: return sendMessage(message, "Link Tidak Ditemukan")

    sira = 0
    inme = sendMessage(message, "✅ Unduhan Selesai")

    for link in linkler:
        sira = sira + 1
        try:
            editMessage(inme, f"🔽 Sedang Memproses Unduhan\n⏳ Mohon Tunggu: {str(sira)} / {len(linkler)}")
            qobuz.handle_url(link)
            for fil in absolutePaths("qobuzdown"):
                if fil.lower().endswith(".jpg"): os.remove(fil)
            editMessage(inme, f'🔼 Mengunggah ke Telegram: {str(sira)} / {len(linkler)} ({len(list(absolutePaths("qobuzdown")))} Lagu)')
            for fil in sorted(absolutePaths("qobuzdown")):
                x:Message = sendMusic(inme, fil)
                if Config.LOG_CHANNEL:
                    try:
                        x.copy(Config.LOG_CHANNEL)
                    except FloodWait as e:
                        time.sleep(e.value)
                        x.copy(Config.LOG_CHANNEL)
                    except Exception as e:
                        LOGGER.error(e)
                os.remove(fil)
        except Exception as e:
            sendMessage(message, helpstr + "\n\n" + str(e))
            continue
    sendMessage(inme, f"✅ Unduhan Selesai {message.from_user.mention}\n📦 Cek Hasil Unduhan @QobuzzDump")
    editMessage(inme, "ᴍᴇɴɢᴜɴɢɢᴀʜ ꜱᴇʟᴇꜱᴀɪ")
    try: shutil.rmtree("qobuzdown")
    except: pass
    os.remove("calisiyor.txt") if os.path.isfile("calisiyor.txt") else print("ok")
