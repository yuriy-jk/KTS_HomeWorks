from aiohttp_apispec import json_schema, response_schema
from marshmallow import Schema, fields

from project_server.apps.admin_user.views import AdminSchema
from project_server.web.view import BaseView, require_auth


class BotUserSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    created = fields.DateTime()
    id = fields.Integer()
    is_banned = fields.Boolean()
    subscriptions = fields.Dict(fields.Str(), fields.DateTime())


class AddView(BaseView):
    @json_schema(BotUserSchema)
    @response_schema(BotUserSchema)
    @require_auth
    async def post(self):
        data = self.request['json']
        return self.store.bot_user.add_user(data['username'], data['password'], data['first_name'], data['last_name'],
                                            data['subscriptions'])


class ListView(BaseView):
    @require_auth
    async def get(self):
        pass


class GetView(BaseView):
    @response_schema(BotUserSchema)
    @require_auth
    async def get(self):
        id = self.request.query['id']
        return self.store.bot_user.get(int(id))


class UpdateView(BaseView):
    @json_schema(BotUserSchema)
    @response_schema(BotUserSchema)
    @require_auth
    async def post(self):
        data = self.request['json']
        return self.store.bot_user.post(**data)
