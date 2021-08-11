from aiohttp import web

from project_server.apps.admin_user.views import AdminLoginView, AdminAddUserView
from project_server.apps.bot_user.views import ListView, GetView, UpdateView, AddView


def setup_urls(app: web.Application):
    app.router.add_view('/admin_user.login', AdminLoginView)
    app.router.add_view('/admin_user.add_user', AdminAddUserView)
    app.router.add_view('/bot_user.list', ListView)
    app.router.add_view('/bot_user.get', GetView)
    app.router.add_view('/bot_user.update', UpdateView)
    app.router.add_view('/bot_user.add', AddView)
