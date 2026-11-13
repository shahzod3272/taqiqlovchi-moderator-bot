import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

# Bot tokeningizni kiriting
TOKEN = "9242529893:AAF9tKC-mjRuBd8whccmXwQszvYDE-wQ_U4"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# 🚫 O'chirilishi KERAK bo'lgan kalit so'zlar
BANNED_KEYWORDS = [
    "do'stlik", "dostlik", "do'stliga", "dostliga", "do'stlikka", "dostlikka",
    "savxoz", "sovxoz", "savxozga", "sovxozga",
    "do'stlik 11", "dostlik 11", "do'stlik-11", 
    "savxozga taksi", "11"
]

# 🛡️ ISTISNOLAR (Jizzax va Toshkentga oid e'lonlar o'chirilmaydi)
EXCEPTIONS = [
    "jizzaxga", "jizzax", 
    "toshkentga", "toshkent", 
    "pagort taksi kerak",
    "jizzaxga taksi", "toshkentga taksi",
    "jizzaxga yo'lovchi", "toshkentga yo'lovchi"
]

# 📝 Xabar o'chirilgandan keyin guruhga yuboriladigan MAXSUS MATN
CUSTOM_REPLY_TEXT = (
    "🚖 **Do‘stlik yoki Savxozga taksi kerakmi?**\n"
    "Buyurtma berish uchun mana bu yerga bosing 👉 @Taksi11ga_bot\n\n"
    "Hammasi juda oson! Bot orqali manzilni yuborsangiz bas, haydovchining o‘zi siz bilan bog‘lanadi. ✅"
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🤖 Assalomu alaykum! Men Do'stlik va Savxoz yo'nalishidagi keraksiz e'lonlarni "
        "tozalovchi va o'rniga o'zimizning e'lonni tashlovchi botman."
    )


# Guruhdagi barcha matnli xabarlarni kuzatish
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def filter_group_messages(message: Message):
    if not message.text:
        return

    text_lower = message.text.lower()

    # 1. 🛡️ Avval ISTISNOLARni tekshiramiz
    for exception_word in EXCEPTIONS:
        if exception_word in text_lower:
            return  # Istisno topildi, xabarga tegilmaydi!

    # 2. 🚫 Taqiqlangan so'zlar bor-yo'qligini tekshiramiz
    should_delete = any(word in text_lower for word in BANNED_KEYWORDS)

    if should_delete:
        try:
            chat_id = message.chat.id
            
            # 1. Keraksiz e'lonni o'chirish
            await message.delete()

            # 2. O'rniga o'zingizning reklama/taklif xabaringizni yuborish
            await bot.send_message(
                chat_id=chat_id,
                text=CUSTOM_REPLY_TEXT,
                parse_mode="Markdown"
            )

        except Exception as e:
            print(f"Xatolik (Botda admin huquqi yo'q bo'lishi mumkin): {e}")


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Moderator bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())