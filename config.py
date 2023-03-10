import logging, os, time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 8778736))
    API_HASH = os.environ.get("API_HASH", "8bb5246d4d5886d6400e13c28714aa4f")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5791370339:AAF9WthEyNM663rxPb2wCYegBPBo7nLE2xk")
    OWNER_ID = int(os.environ.get('OWNER_ID', 1432132252)) # give your owner id # if given 0 shell will not works
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "-1001625028324").split()] # if open to everyone give 0
    AUTH_IDS.append(OWNER_ID)
    QOBUZ_MAIL = os.environ.get("QOBUZ_MAIL", "xikehahi@lyft.live")
    QOBUZ_PASS = os.environ.get("QOBUZ_PASS", "Qobuz2023")
    QOBUZ_QUAL = int(os.environ.get("QOBUZ_QUAL", 27))
    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY', None)
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
    UPDATE_ALL = bool(os.environ.get("UPDATE_ALL", True))
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001686340058")
    botStartTime = time.time() # dont touch
