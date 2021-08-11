import pprint

from aiohttp import web
from aiohttp_apispec import json_schema, response_schema, request_schema
from marshmallow import Schema, fields
from marshmallow.fields import Date

from project_server.web.view import BaseView, require_auth


class AdminSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    created = fields.DateTime()


class AdminLoginView(BaseView):
    @json_schema(AdminSchema)
    @response_schema(AdminSchema)
    async def post(self):
        data = self.request['json']
        user = self.store.admin.login(data['username'], data['password'])
        session = self.store.session.generate_session(user.username)
        response = web.json_response(AdminSchema().dump(user))
        response.set_cookie('session_id', session.id)
        return response


class AdminAddUserView(BaseView):

    @json_schema(AdminSchema)
    @response_schema(AdminSchema)
    @require_auth
    async def post(self):
        data = self.request['json']
        return self.store.admin.add_user(data['username'], data['password'], data['first_name'], data['last_name'])

