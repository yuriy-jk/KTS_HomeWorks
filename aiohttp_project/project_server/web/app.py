import datetime
import json

from typing import Optional, Mapping, NoReturn

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from marshmallow import ValidationError, Schema

from project_server.store import Store
from project_server.web.middlewares import resp_middleware, error_mw, auth_mw
from project_server.web.urls import setup_urls


# python -m aiohttp.web -H localhost -P 8081 project_server.web.app:create_app

def my_error_handler(
        error: ValidationError,
        req: web.Request,
        schema: Schema,
        error_status_code: Optional[int] = None,
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


def create_app(argv):
    app = web.Application()
    setup_urls(app)
    app['store'] = Store()
    app.middlewares.extend([error_mw, validation_middleware, resp_middleware, auth_mw])
    setup_aiohttp_apispec(
        app=app,
        title="My Documentation",
        version="v1",
        swagger_path="/docs",
        error_callback=my_error_handler
    )

    return app


web.run_app(create_app(argv=1))
