import os
import asyncio
import secrets
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pyrogram import Client, filters, types
from config import Config
from database import db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await bot.start()
    me = await bot.get_me(); Config.BOT_USERNAME = me.username
    print("🚀 Ghost Streamer Bot is Online!")
    yield
    await bot.stop()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
bot = Client("GhostBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

@bot.on_message(filters.private & (filters.document | filters.video))
async def file_handler(client, message):
    sent_msg = await message.copy(chat_id=Config.STORAGE_CHANNEL)
    unique_id = secrets.token_urlsafe(8)
    await db.save_link(unique_id, sent_msg.id)
    verify_link = f"https://t.me/{Config.BOT_USERNAME}?start=verify_{unique_id}"
    btn = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("🔗 Open Link", url=verify_link)]])
    await message.reply_text("✅ **File Secured! Click below to get your link:**", reply_markup=btn)

@app.get("/show/{unique_id}", response_class=HTMLResponse)
async def show_page(request: Request, unique_id: str):
    return templates.TemplateResponse("show.html", {"request": request})

@app.get("/api/file/{unique_id}")
async def get_file_api(unique_id: str):
    mid = await db.get_link(unique_id)
    msg = await bot.get_messages(Config.STORAGE_CHANNEL, mid)
    media = msg.document or msg.video
    return JSONResponse({
        "file_name": media.file_name,
        "file_size": f"{round(media.size / (1024*1024), 2)} MB",
        "direct_dl_link": f"{Config.BASE_URL}/dl/{unique_id}"
    })

@app.get("/dl/{unique_id}")
async def stream_file(unique_id: str):
    mid = await db.get_link(unique_id)
    msg = await bot.get_messages(Config.STORAGE_CHANNEL, mid)
    media = msg.document or msg.video
    async def generate():
        async for chunk in bot.download_media(media, in_memory=True): yield chunk
    return StreamingResponse(generate(), media_type=media.mime_type)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
