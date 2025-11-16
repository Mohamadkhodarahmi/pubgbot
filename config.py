import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', '').split(',') if id]
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID', '')
TARGET_GROUP_ID = os.getenv('TARGET_GROUP_ID', '')

# Telegram Bypass Configuration (برای دور زدن فیلترینگ در ایران)
# می‌توانید از ورکر عمومی استفاده کنید یا خودتان یک ورکر بسازید
# ورکر عمومی: https://public-telegram-bypass.solyfarzane9040.workers.dev/
# یا ورکر خودتان را در Cloudflare Workers بسازید
TELEGRAM_BYPASS_URL = os.getenv('TELEGRAM_BYPASS_URL', '')
USE_BYPASS = os.getenv('USE_BYPASS', 'false').lower() == 'true'

# Payment Gateway Configuration (Zarinpal)
ZARINPAL_MERCHANT_ID = os.getenv('ZARINPAL_MERCHANT_ID', '')
ZARINPAL_SANDBOX = os.getenv('ZARINPAL_SANDBOX', 'true').lower() == 'true'
ZARINPAL_CALLBACK_URL = os.getenv('ZARINPAL_CALLBACK_URL', '')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pubg_bot.db')
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# Application Configuration
DEFAULT_PRICE_PER_PLAYER = int(os.getenv('DEFAULT_PRICE_PER_PLAYER', '100000'))  # in Rials
MAX_PLAYERS_PER_TEAM = 4
MIN_PLAYERS_PER_TEAM = 3
TOTAL_SLOTS = 16  # 16 sections, 4 players each = 64 total players
PLAYERS_PER_SECTION = 4

# Webhook Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))

# Panel Configuration
PANEL_SECRET_KEY = os.getenv('PANEL_SECRET_KEY', 'your-secret-key-here')
PANEL_PORT = int(os.getenv('PANEL_PORT', '5000'))

# Language and Timezone
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'fa')
DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Asia/Tehran')
