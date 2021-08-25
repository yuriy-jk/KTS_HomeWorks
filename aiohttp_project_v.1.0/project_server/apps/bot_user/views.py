from urllib.parse import parse_qs

from aiohttp_apispec import json_schema, response_schema, request_schema
from marshmallow import Schema

from apps.bot_user.schema import ListBotUserSchemaResponse, RequestBotUserSchema, ResponseBotUserSchema, UpdateBotUserSchema, \
    GetBotUserSchema, ListBotUserSchemaRequest
from web.view import BaseView, require_auth


# class AddView(BaseView):
#     @json_schema(RequestBotUserSchema.Schema)
#     @response_schema(ResponseBotUserSchema.Schema)
#     @require_auth
#     async def post(self):
#         data = self.request['json']
#         return await self.store.bot_user.add_user(data.username, data.password, data.first_name,
#                                                   data.last_name,
#                                                   data.subscriptions)


class ListView(BaseView):
    @request_schema(ListBotUserSchemaRequest.Schema)
    @response_schema(ListBotUserSchemaResponse.Schema)
    @require_auth
    async def get(self):
        params = ListBotUserSchemaRequest.Schema().dump(self.request['data'])
        return await self.store.bot_user.list(params)


class GetView(BaseView):
    @json_schema(GetBotUserSchema.Schema)
    @response_schema(ResponseBotUserSchema.Schema)
    @require_auth
    async def get(self):
        data = self.request['json']
        return await self.store.bot_user.get(data.id)


class UpdateView(BaseView):
    @json_schema(UpdateBotUserSchema.Schema)
    @response_schema(ResponseBotUserSchema.Schema)
    @require_auth
    async def post(self):
        data = self.request['json']
        return await self.store.bot_user.post(data)
