from aiohttp import web


def setup_urls(app: web.Application):
    from apps.admin_user.urls import setup_admin_urls

    setup_admin_urls(app)

    from apps.bot_user.urls import setup_botuser_urls

    setup_botuser_urls(app)
