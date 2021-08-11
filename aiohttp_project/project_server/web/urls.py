from aiohttp import web


def setup_urls(app: web.Application):
    from project_server.apps.admin_user.urls import setup_urls

    setup_urls(app)
