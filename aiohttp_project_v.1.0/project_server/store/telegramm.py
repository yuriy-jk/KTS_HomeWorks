import datetime
import string

from aiogram.types import ContentType
from aiohttp import web

from apps.bot_user.models import User, Subscriptions
from apps.bot_user.schema import SubscriptionsSchema
from store.accessor import Accessor
from aiogram import types

from store.bot import dp
from store.gino import db
from web.exceptions import AlreadyExists, Error


class TelegrammAccessor(Accessor):
    def __init__(self, app: web.Application):
        super().__init__(app)

    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        username = message.chat.username
        subscribe_btn = types.KeyboardButton('/subscribe')
        start_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        start_kb.add(subscribe_btn)
        welcome_text = f'Добро пожаловать, {username}, этот бот присылает ссылки на статьи из Хабра по интересующим ' \
                       f'тебя ' \
                       f'темам.\nЖми подписаться! '
        await message.answer(welcome_text, reply_markup=start_kb)

    @dp.message_handler(commands=['subscribe'])
    async def subscribe(message: types.Message):
        username = message.chat.username
        is_user = await User.query.where(User.username == username).gino.first()
        tags_list_btn = types.KeyboardButton('/Мои_подписки')
        tags_add_btn = types.KeyboardButton('/Добавить_подписки')
        tags_update_btn = types.KeyboardButton('/Изменить_подписки')
        tags_service_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        tags_service_kb.add(tags_list_btn, tags_add_btn, tags_update_btn)
        if is_user is not None:
            await message.answer(f'Спасибо {username}, но ты уже зарегестрирован!', reply_markup=tags_service_kb)
            raise AlreadyExists

        first_name = message.chat.first_name
        last_name = message.chat.last_name
        date = message.date
        async with db.transaction():
            try:
                await User.create(username=username, first_name=first_name,
                                  last_name=last_name, created=date, is_banned='False')
            except Exception:
                raise Error
        await message.answer(f'Спасибо {username}, я тебя зарегестрировал!'
                             f'Теперь ты можешь добавлять и редактировать свои подписки', reply_markup=tags_service_kb)

    @dp.message_handler(commands=['Добавить_подписки'])
    async def tags_input(message: types.Message):
        await message.answer(f'Введи интересующие тебя темы через пробел\n'
                             f'Например: python java ruby')

    @dp.message_handler(commands=['Мои_подписки'])
    async def tags_input(message: types.Message):
        username = message.chat.username
        user = await User.query.where(User.username == username).gino.first()
        subs = await Subscriptions.query.where(Subscriptions.user_id == user.id).gino.load(Subscriptions).all()
        response = {}
        if len(subs) > 0:
            for sub in subs:
                q = SubscriptionsSchema.Schema().dump(sub)
                response[q['tag']] = q['schedule']
            await message.answer(f'Твои подписки:\n{response}')

        else:
            await message.answer(f'У тебя еще нет подписок')

            await message.answer(f'Введи интересующие тебя темы через пробел\n'
                                 f'Например: python java ruby')

    @dp.message_handler(content_types=ContentType.TEXT)
    async def tags_handler(message: types.Message):
        text = message.text
        if any((c in string.punctuation) for c in text):
            await message.answer(f'Через пробел!')
        else:
            tags = text.split()
            username = message.chat.username
            user = await User.query.where(User.username == username).gino.first()
            schedule = datetime.datetime.now()
            async with db.transaction():
                try:
                    for tag in tags:
                        await Subscriptions.create(user_id=user.id, tag=tag.lower(), schedule=schedule)
                except Exception:
                    raise Error

            await message.answer(f'Подписки добавлены!')
