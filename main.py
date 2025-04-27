import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from config import BOT_TOKEN, WEBHOOK_URL

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

questions = [
    ("Луч, исходящий из вершины угла и делящий его на два равных угла, называется…", "биссектриса"),
    ("Сколько материков на планете Земля", "шесть"),
    ("У древних греков — Афина, а у древних римлян — …", "минерва"),
    ("Вид обуви с закрытой шнуровкой (в отличие от дерби)", "хогвартсы"),
    ("Продолжите фразу: Классика…", "ебаная"),
    ("В чем измеряется сила тока", "ампер"),
    ("Когда произошло восстание декабристов?", "1825"),
    ("Кто спел строки: I could play the doctor...", "леди гага"),
    ("Самый неприятный человек в мире", "толчок"),
    ("Когда было отменено постановление о приостановлении деятельности Засёрной коллегии?", "26.11.2024"),
    ("Самая лучшая карбонара в мире?", "торговая площадь"),
    ("Где находятся говнянные баребухи?", "на яйцах"),
    ("Лучший мужик в КР по мнению Лизы", "голод"),
    ("Чего нам обычно хочется за десять минут до собрания засёрной коллегии?", "счастья"),
    ("Главный герой сказок 1000 и 1 ночи", "али баба"),
]

final_message = """
Ура, эта встратая викторинка закончилась!
Во-первых, спасибо, что ты есть у нас, прекрасная такая. Ты умеешь зажигать людей и объединять их вокруг себя (просто посмотри на наш клуб засёрышей). Сияй, поражай, вдохновляй - ни секунды не сомневайся в том, что ты лучшая (а если кто-то думает иначе, то дорога им на наше заседание, мы их там хорошенечко обосрем).
Во-вторых, иногда банан - это просто банан. Не стоит придавать ему слишком большую важность. В конце-концов, самое важное - это как ты себя ощущаешь, и ни одна ситуация не должна заставлять тебя чувствовать себя недостаточно хорошей для чего-то.
Будут солнце и грозы,
Будут девичьи слезы,
Станут взрослыми дети,
Будет счастье на свете.
Все хорошо будет, короче. И бизнес-идейки однажды реализуются, и с дырявой конторы ты свалишь.
Ну, может, еще встретимся потом. Встретимся, когда пойдет дождь.
С днем рождения!
"""

user_states = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    user_states[message.from_user.id] = {"q_index": 0}
    await message.answer("Хай! Ну что, погнали проверим твои знания!")
    await ask_question(message.from_user.id)

async def ask_question(user_id):
    state = user_states.get(user_id)
    if state is None:
        return
    if state["q_index"] < len(questions):
        question_text = questions[state["q_index"]][0]
        await bot.send_message(user_id, question_text)
    else:
        await bot.send_message(user_id, final_message)
        user_states.pop(user_id)

@dp.message()
async def answer(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state:
        await message.answer("Нажми /start, чтобы быстрее покончить с этим.")
        return

    correct_answer = questions[state["q_index"]][1].lower()
    user_answer = message.text.strip().lower()

    if user_answer == correct_answer:
        state["q_index"] += 1
        await ask_question(user_id)
    else:
        await message.answer("Че тупим? Подумай еще")

async def main():
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        from aiohttp import web

        async def handler(request):
            body = await request.read()
            update = types.Update.model_validate_json(body)
            await dp.feed_update(bot, update)
            return web.Response()

        app = web.Application()
        app.router.add_post("/", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()

        print("Bot is running via webhook...")
        while True:
            await asyncio.sleep(3600)
    else:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())