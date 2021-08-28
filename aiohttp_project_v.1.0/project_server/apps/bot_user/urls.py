from aiohttp import web

from apps.bot_user.views import ListView, GetView, UpdateView, AddView


def setup_botuser_urls(app: web.Application):
    app.router.add_view("/bot_user.list", ListView)
    app.router.add_view("/bot_user.get", GetView)
    app.router.add_view("/bot_user.update", UpdateView)
    app.router.add_view("/bot_user.add", AddView)
