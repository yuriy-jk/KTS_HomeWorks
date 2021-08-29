from datetime import datetime

from aiogram.types import ContentType
from aiohttp import web

from apps.bot_user.accessor import UserAccessor
from apps.bot_user.models import User, Subscriptions
from apps.bot_user.schema import SubscriptionsSchema, UpdateBotUserSchema
from store.accessor import Accessor
from aiogram import types

from store.bot import dp, bot
from store.gino import db
from web.exceptions import AlreadyExists, Error

import pytz

tzmoscow = pytz.timezone('Europe/Moscow')


class TelegramAccessor(Accessor):
    def __init__(self, app: web.Application):
        super().__init__(app)

    @dp.message_handler(commands=["start", "help"])
    async def send_welcome(message: types.Message):
        username = message.chat.username
        subscribe_btn = types.KeyboardButton("/subscribe")
        start_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        start_kb.add(subscribe_btn)
        welcome_text = (
            f"Добро пожаловать, {username}, этот бот присылает ссылки на статьи из Хабра по интересующим "
            f"тебя "
            f"темам.\nЖми подписаться! "
        )
        await message.answer(welcome_text, reply_markup=start_kb)

    @dp.message_handler(commands=["subscribe"])
    async def subscribe(message: types.Message):
        username = message.chat.username
        is_user = await User.query.where(User.username == username).gino.first()
        tags_list_btn = types.KeyboardButton("/Мои_подписки")
        tags_add_btn = types.KeyboardButton("/Добавить_подписки")
        tags_service_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        tags_service_kb.add(tags_list_btn, tags_add_btn)
        if is_user is not None:
            await message.answer(
                f"Спасибо {username}, но ты уже зарегестрирован!",
                reply_markup=tags_service_kb,
            )
            raise AlreadyExists

        first_name = message.chat.first_name
        last_name = message.chat.last_name
        date = datetime.now(tzmoscow)
        db_date = date.replace(tzinfo=None)
        chat_id = message.chat.id
        async with db.transaction():
            try:
                await User.create(
                    chat_id=chat_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    created=db_date,
                    is_banned="False",
                )
            except Exception:
                raise Error
        await message.answer(
            f"Спасибо {username}, я тебя зарегестрировал!"
            "Теперь ты можешь добавлять и редактировать свои подписки",
            reply_markup=tags_service_kb,
        )

    @dp.message_handler(commands=["Добавить_подписки"])
    async def tags_input(message: types.Message):
        await message.answer(
            "Введи интересующие тебя тему и расписание через запятую\n"
            "Например: python 13:00, java 13:00"
        )

    @dp.message_handler(commands=["Мои_подписки"])
    async def my_tags(message: types.Message):
        username = message.chat.username
        user = await User.query.where(User.username == username).gino.first()
        subs = (
            await Subscriptions.query.where(Subscriptions.user_id == user.id)
                .gino.load(Subscriptions)
                .all()
        )
        response = {}
        if len(subs) > 0:
            for sub in subs:
                q = SubscriptionsSchema.Schema().dump(sub)
                response[q["tag"]] = q["schedule"]
            await message.answer(f"Твои подписки:\n{response}")

        else:
            await message.answer("У тебя еще нет подписок")

            await message.answer(
                "Введи интересующие тебя тему и расписание через запятую\n"
                "Например: python 13:00, java 13:00"
            )

    @dp.message_handler(content_types=ContentType.TEXT)
    async def tags_handler(message: types.Message):
        text = message.text.split(",")
        text = [sub.split() for sub in text]
        subscriptions = {sub[0]: sub[1] for sub in text}
        user = await User.query.where(
            User.username == message.chat.username
        ).gino.first()
        user_id = user.id
        data = {"id": user_id, "subscriptions": subscriptions}
        await UserAccessor.post(UpdateBotUserSchema.Schema().load(data=data))
        await message.answer("Подписки добавлены!")

    @dp.message_handler(content_types=["text"])
    async def send_links(self, chat_id: int, links: list):
        await bot.send_message(chat_id, links)

    @dp.message_handler(content_types=["text"])
    async def send_empty_links(self, chat_id: int):
        text = 'Я не нашел свежих статей'
        await bot.send_message(chat_id, text)
