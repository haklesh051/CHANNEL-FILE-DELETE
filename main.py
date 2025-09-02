import os
from pyrogram import Client, filters

# -------------------------------
# Telegram API setup
# -------------------------------
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

OWNER_ID = 7681589139  # Your personal Telegram ID
CHANNEL_USERNAME = "@haklesh"  # Your channel username

deleted_count = 0  # Global counter

app = Client("delete_failed_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# -------------------------------
# Helper: check if message is target
# -------------------------------
def is_target_message(message):
    if message.text:
        return message.text.startswith("⚠️Downloading Failed⚠️") or message.text.startswith("📩 Uploading Video 📩")
    return False

# -------------------------------
# Delete old messages
# -------------------------------
async def delete_existing_messages():
    global deleted_count
    async for message in app.get_chat_history(CHANNEL_USERNAME):
        if is_target_message(message):
            try:
                await message.delete()
                deleted_count += 1
                print(f"Deleted old message: {message.message_id} | Total deleted: {deleted_count}")
            except Exception as e:
                print(f"Error deleting message {message.message_id}: {e}")

# -------------------------------
# Delete new incoming messages
# -------------------------------
@app.on_message(filters.channel)
async def delete_new_messages(client, message):
    global deleted_count
    if is_target_message(message):
        try:
            await message.delete()
            deleted_count += 1
            print(f"Deleted new message: {message.message_id} | Total deleted: {deleted_count}")
        except Exception as e:
            print(f"Error deleting new message {message.message_id}: {e}")

# -------------------------------
# /status command - owner only
# -------------------------------
@app.on_message(filters.private & filters.command("status"))
async def status(client, message):
    if message.from_user.id == OWNER_ID:
        await message.reply_text(f"✅ Total deleted messages: {deleted_count}")
    else:
        await message.reply_text("❌ You are not authorized.")

# -------------------------------
# /reset command - owner only
# -------------------------------
@app.on_message(filters.private & filters.command("reset"))
async def reset_counter(client, message):
    global deleted_count
    if message.from_user.id == OWNER_ID:
        deleted_count = 0
        await message.reply_text("♻️ Deleted counter has been reset.")
    else:
        await message.reply_text("❌ You are not authorized.")

# -------------------------------
# Run bot
# -------------------------------
app.start()
app.loop.run_until_complete(delete_existing_messages())  # Delete old messages first
print(f"✅ Finished deleting existing messages. Total deleted: {deleted_count}")
app.idle()
