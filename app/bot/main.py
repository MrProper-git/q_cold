import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from app.shared.database import new_session, LeadsModel
from sqlalchemy import select

from app.config import bot_api, admin_id

session = AiohttpSession(
    proxy="socks5://185.131.204.212:1080"  # замени на свой
)

bot = Bot(token=bot_api)
dp = Dispatcher()



async def check_new_leads():
    """Фоновая задача: проверяет новые заявки каждые 3 секунды"""
    while True:
        try:
            async with new_session() as session:
                # Ищем непрочитанные заявки
                result = await session.execute(
                    select(LeadsModel).where(LeadsModel.notified == False)
                )
                leads = result.scalars().all()

                for lead in leads:
                    # Отправляем админу
                    message = (
                        f"🆕 **Новая заявка!**\n\n"
                        f"👤 **Имя:** {lead.name}\n"
                        f"📞 **Контакт:** {lead.contact}\n"
                        f"📝 **Текст:** {lead.text}\n"
                        f"🆔 **ID заявки:** {lead.id}"
                    )
                    await bot.send_message(admin_id, message, parse_mode="Markdown")

                    # Помечаем как отправленное
                    lead.notified = True
                    await session.commit()

                    print(f"✅ Отправлена заявка #{lead.id}")

        except Exception as e:
            print(f"❌ Ошибка в боте: {e}")

        # Пауза перед следующим циклом
        await asyncio.sleep(3)


async def main():
    asyncio.create_task(check_new_leads())
    #dp.include_router()
    await dp.start_polling(bot)
    print("Бот запущен")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

