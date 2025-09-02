import asyncio
from pyrogram import Client, filters

# -------------------------------
# Telegram API & Userbot Setup
# -------------------------------
api_id = int(input("23977225"))        # Telegram API ID
api_hash = input("969c399e6aea5032314a2e17cab428be")         # Telegram API Hash
PHONE_NUMBER = input("7300209558") # Telegram account phone
OWNER_ID = int(input("7681589139")) # Personal Telegram ID
CHANNEL_USERNAME = "@haklesh"                 # Channel username

deleted_count = 0  # Global counter

app = Client("userbot_session", api_id=api_id, api_hash=api_hash, phone_number=PHONE_NUMBER)

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
async def delete_old_messages():
    global deleted_count
    async for message in app.get_chat_history(CHANNEL_USERNAME, limit=None):
        if is_target_message(message):
            try:
                await message.delete()
                deleted_count += 1
                print(f"Deleted old message: {message.message_id} | Total deleted: {deleted_count}")
            except Exception as e:
                print(f"Error deleting message {message.message_id}: {e}")

# -------------------------------
# Delete new messages
# -------------------------------
@app.on_message(filters.chat(CHANNEL_USERNAME))
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
# Owner commands
# -------------------------------
@app.on_message(filters.private & filters.command("status"))
async def status(client, message):
    if message.from_user.id == OWNER_ID:
        await message.reply_text(f"✅ Total deleted messages: {deleted_count}")
    else:
        await message.reply_text("❌ You are not authorized.")

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
async def main():
    await app.start()
    print("✅ Userbot started. Deleting old messages...")
    await delete_old_messages()
    print(f"✅ Finished deleting old messages. Total deleted: {deleted_count}")
    await app.idle()

asyncio.run(main())
