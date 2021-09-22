import json
from typing import Optional, Mapping, NoReturn
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from marshmallow import ValidationError

from store import Store
from web.middlewares import resp_middleware, error_mw, auth_mw
from web.urls import setup_urls


# python -m aiohttp.web -H localhost -P 8081 project_server.web.app:create_app


def my_error_handler(
    error: ValidationError,
    error_headers: Optional[Mapping[str, str]] = None,
) -> NoReturn:
    raise web.HTTPBadRequest(
        body=json.dumps(
            {
                "code": "invalid_data",
                "description": "Invalid data",
                "data": error.messages,
            }
        ),
        headers=error_headers,
        content_type="application/json",
    )


def setup_store(app: web.Application):
    store = Store(app)
    app["store"] = store
    store.setup()


def create_app():
    app = web.Application()
    setup_store(app)
    setup_urls(app)
    app.middlewares.extend([error_mw, validation_middleware, resp_middleware, auth_mw])
    setup_aiohttp_apispec(
        app=app,
        title="My Documentation",
        version="v1",
        swagger_path="/docs",
        error_callback=my_error_handler,
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app())
