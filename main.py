import os
from pyrogram import Client, filters

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("delete_failed_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.channel & filters.regex(r"^⚠️Downloading Failed⚠️"))
async def delete_failed(client, message):
    try:
        if message.media:
            await message.delete()
            print(f"Deleted failed file + message: {message.message_id}")
        else:
            await message.delete()
            print(f"Deleted failed message: {message.message_id}")
    except Exception as e:
        print(f"Error: {e}")

app.run()
