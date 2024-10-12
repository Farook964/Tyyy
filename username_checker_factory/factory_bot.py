from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import os

# إعدادات المصنّع
api_id = 29677860
api_hash = '785da04e1d7d75c744632dacd6134d34'
factory_bot_token = '7917495652:AAGBQYLsIKaoQ9sowoJ1e1bpOutnRbX-C9I'  # ضع توكن بوت المصنع هنا

# قم بإنشاء مجلد لتخزين الجلسات
if not os.path.exists("sessions"):
    os.makedirs("sessions")

app = Client("factory_bot", api_id, api_hash, bot_token=factory_bot_token)

@app.on_message(filters.command("start", prefixes="/"))
async def handle_start(client, message):
    await message.reply(
        "👋 **أهلاً بك في مصنع سورس SB لصناعة بوتات فحص يوزرات تلغرام!**\n"
        "🔧 **استخدم الأوامر التالية لإدارة البوتات:**\n"
        "📌 /add_bot <token> - **لإضافة بوت جديد.**\n"
        "📌 /delete_bot <session_name> - **لحذف بوت.**\n"
        "📌 /help - **للحصول على المساعدة.**"
    )

@app.on_message(filters.command("add_bot", prefixes="/"))
async def add_bot(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ **الرجاء توفير توكن البوت.**")
        return

    bot_token = message.command[1]
    session_name = bot_token.split(":")[0]  # استخدام جزء من التوكن كاسم الجلسة

    
    with open(f"sessions/{session_name}.py", "w") as f:
        f.write(f"""
       
from pyrogram import Client, filters
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, FloodWait
import asyncio
import string
import itertools

api_id = {api_id}
api_hash = '{api_hash}'
bot_token = '{bot_token}'
session_name = '{session_name}'

app = Client(session_name, api_id, api_hash, bot_token=bot_token)
async def check_usernames(usernames, message):
    global running, checked_count, total_usernames
    available_usernames = []
    total_usernames = len(usernames)
    checked_count = 0

    for username in usernames:
        if not running:
            await message.reply("✅ **تـم إيـقـاف الـفـحـص.**")
            return

        try:
            user = await app.get_users(username)
            result_message = f"❌ **الـيـوزر @{username} مـسـتـخـدم 😐**"
            await message.reply(result_message)

        except UsernameNotOccupied:
            available_message = f"✅ **الـيـوزر @{username} مـتـاح 🥳**"
            await message.reply(available_message)
            available_usernames.append(username)

        except FloodWait as e:
            wait_time = e.x + 5
            await message.reply(f"⚠️ **مطلوب الانتظار لمدة {wait_time} ثانية بسبب FloodWait.**")
            await asyncio.sleep(wait_time)
            continue

        except UsernameInvalid:
            error_message = f"⚠️ **الـيـوزر @{username} غـيـر صـالـح.**"
            await message.reply(error_message)

        except Exception as e:
            error_message = f"⚠️ **حـدث خـطـأ أثـنـاء فـحـص @{username}: {e}**"
            await message.reply(error_message)

        await asyncio.sleep(5)  
        checked_count += 1

    if available_usernames:
        available_str = "\n".join([f"@{uname}" for uname in available_usernames])
        await message.reply(f"✅ **الأسـمـاء الـمـتـاحـة:**\n{available_str}")
    else:
        await message.reply("⚠️ **لـم يـتـم الـعـثـور عـلـى أسـمـاء مـتـاحـة.**")

    running = False

if __name__ == '__main__':
    app.run()
""")
    
    await message.reply(f"✅ **تم إضافة البوت بنجاح: {session_name}**")

@app.on_message(filters.command("delete_bot", prefixes="/"))
async def delete_bot(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ **الرجاء توفير اسم الجلسة لحذف البوت.**")
        return

    session_name = message.command[1]
    try:
        os.remove(f"sessions/{session_name}.py")
        await message.reply(f"✅ **تم حذف البوت: {session_name} بنجاح.**")
    except FileNotFoundError:
        await message.reply("⚠️ **اسم الجلسة غير موجود.**")

@app.on_message(filters.command("help", prefixes="/"))
async def handle_help(client, message):
    await message.reply(
        "👋 **أهلاً بك في مصنع سورس SB!**\n"
        "📌 /add_bot <token> - **لإضافة بوت جديد.**\n"
        "📌 /delete_bot <session_name> - **لحذف بوت.**"
    )

if __name__ == '__main__':
    app.run()
