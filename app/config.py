import os
from dotenv import load_dotenv

load_dotenv()

bot_api = os.getenv('BOT_API')
admin_id = os.getenv('ADMIN_ID')