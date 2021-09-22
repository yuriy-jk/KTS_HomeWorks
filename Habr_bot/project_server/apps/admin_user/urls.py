from aiohttp import web

from apps.admin_user.views import AdminLoginView, AdminAddUserView


def setup_admin_urls(app: web.Application):
    app.router.add_view("/admin_user.login", AdminLoginView)
    app.router.add_view("/admin_user.add_user", AdminAddUserView)
