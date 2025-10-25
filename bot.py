# bot.py (FINAL CLEAN VERSION)

import os
import asyncio
from pyrogram import Client
from config import Config

# Dictionaries for multi-client setup
multi_clients = {}
work_loads = {}

# Pyrogram ko batao ki saare handlers 'plugins' folder ke andar hain
plugins = dict(root="plugins")

# Bot client ko define karo
bot = Client(
    name="SimpleStreamBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    plugins=plugins,  # <-- Yahan plugins ko register karo
    workdir="sessions"
)

# --- Multi-Client Initialization Logic ---
class TokenParser:
    @staticmethod
    def parse_from_env():
        return {
            c + 1: t
            for c, (_, t) in enumerate(
                filter(lambda n: n[0].startswith("MULTI_TOKEN"), sorted(os.environ.items()))
            )
        }

async def start_client(client_id, bot_token):
    try:
        print(f"Attempting to start Client: {client_id}")
        # Multi-clients ko plugins ki zaroorat nahi hai, isliye unhe no_updates=True ke saath start karo
        client = await Client(
            name=str(client_id), api_id=Config.API_ID, api_hash=Config.API_HASH,
            bot_token=bot_token, no_updates=True, in_memory=True
        ).start()
        work_loads[client_id] = 0
        multi_clients[client_id] = client
        print(f"Client {client_id} started successfully.")
    except Exception as e:
        print(f"!!! CRITICAL ERROR: Failed to start Client {client_id} - Error: {e}")

async def initialize_clients(main_bot_instance):
    multi_clients[0] = main_bot_instance
    work_loads[0] = 0
    print("Main bot instance registered for work.")

    all_tokens = TokenParser.parse_from_env()
    if not all_tokens:
        print("No additional clients found. Using default bot only.")
        return
    
    print(f"Found {len(all_tokens)} extra clients. Starting them with a delay.")
    for i, token in all_tokens.items():
        await start_client(i, token)
        await asyncio.sleep(2)

    if len(multi_clients) > 1:
        print(f"Multi-Client Mode Enabled. Total Clients: {len(multi_clients)}")
