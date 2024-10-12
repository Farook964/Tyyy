
from pyrogram import Client, filters
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, FloodWait
import asyncio
import string
import itertools
from config import api_id, api_hash, bot_token, session_name
from factory_bot import generate_usernames, generate_custom_usernames, check_usernames

app = Client(session_name, api_id, api_hash, bot_token=bot_token)

running = False
checked_count = 0
total_usernames = 0

@app.on_message(filters.command("start", prefixes="/"))
async def handle_start(client, message):
    await message.reply(
        "👋 **مـرحـبـاً بـك فـي بـوت سـورس𝐒𝐁𓁒 لـفـحـص أسـمـاء الـمـسـتـخـدمـيـن!**\n"
        "💡 **اسـتـخـدم الأوامـر الـتـالـيـة لـلـبـدء:**\n"
        "📌 /check <حـرف> - **لـفـحـص الأسـمـاء الـثـلاثـيـة.**\n"
        "📌 /custom_check <حـرفـيـن> - **لـفـحـص الأسـمـاء الـربـاعـيـة.**\n"
        "📌 /check_us <قـاعـدة> - **لـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة الـخـاصـة بـك.**\n"
        "📌 /status - **لـمـعـرفـة تـقـدم الـفـحـص الـحـالـي.**\n"
        "📌 /stop - **لإيـقـاف الـفـحـص الـجـاري.**\n"
        "📌 /help - **لـعـرض قـائـمـة الأوامـر.**"
    )

@app.on_message(filters.command("check", prefixes="/"))
async def handle_check(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالـفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـبـحـث. مـثـال: /check S**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) != 1:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفًـا واحـدًا فـقـط.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسماء الـثـلاثـيـة بـنـاءً عـلـى الـقـاعـدة `{base}`. انـتـظـر قـلـيـلاً...**")

    usernames = await generate_usernames(base.lower())
    await check_usernames(usernames, message)

@app.on_message(filters.command("custom_check", prefixes="/"))
async def handle_custom_check(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـفـحـص. مـثـال: /custom_check Aa**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) != 2:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفـيـن فـقـط.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسـمـاء الـربـاعـيـة بـنـاءً عـلـى الـقـاعـدة `{base}`. انـتـظــر قـلـيـلاً...**")

    usernames = await generate_custom_usernames(base.lower())
    await check_usernames(usernames, message)

@app.on_message(filters.command("check_us", prefixes="/"))  
async def handle_check_us(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالـفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـفـحـص. مـثـال: /check_us dddd**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) < 1:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفًـا واحـدًا أو أكـثـر.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة `{base}`. انـتـظـر قـلـيـلاً...**")

    usernames = []
    for char in string.ascii_lowercase:
        usernames.append(f"@{base}{char}")  

    for number in range(1, 11):
        usernames.append(f"@{base}{number}")  

    await check_usernames(usernames, message)

@app.on_message(filters.command("stop", prefixes="/"))
async def handle_stop(client, message):
    global running
    if not running:
        await message.reply("⚠️ **لا يـوجـد فـحـص قـيـد الـتـشـغـيـل.**")
    else:
        running = False
        await message.reply("✅ **تـم إيـقـاف الـفـحـص.**")

@app.on_message(filters.command("status", prefixes="/"))
async def handle_status(client, message):
    if running:
        progress = (checked_count / total_usernames) * 100 if total_usernames > 0 else 0
        await message.reply(f"🔍 **الـفـحـص قـيـد الـتـقـدم... {progress:.2f}% تـم فـحـصـهـا 📊**")
    else:
        await message.reply("⚠️ **لا يـوجـد فـحـص قـيـد الـتـشـغـيـل حـالـيـاً.**")

@app.on_message(filters.command("help", prefixes="/"))
async def handle_help(client, message):
    await message.reply(
        "👋 **أهـلاً بـك فـي بـوت سـورس 𝐒𝐁𓁒 🫂 لـفـحـص الأسـمـاء هـذا الـمـلـف والـبـوت حـقـوقـه كامـلـة لـلـمـطـورة سـحـر 𝐒𝐁𓁒👩🏻‍💻  إلـيـك الأوامـر الـمـتـاحـة:**\n"
        "📌 /check <حـرف> - **لـفـحـص الأسـمـاء الـثـلاثـيـة.**\n"
        "📌 /custom_check <حـرفـيـن> - **لـفـحـص الأسـمـاء الـربـاعـيـة.**\n"
        "📌 /check_us <قـاعـدة> - **لـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة الـخـاصـة بـك.**\n"
        "📌 /status - **لـمـعـرفـة تـقـدم الـفـحـص الـحـالـي.**\n"
        "📌 /stop - **لإيـقـاف الـفـحـص الـجـاري.**\n"
        "📌 /help - **لـعـرض قـائـمـة الأوامـر.**"
    )

if __name__ == '__main__':
    app.run()
``
