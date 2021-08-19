from aiohttp_apispec import json_schema, response_schema
from urllib.parse import parse_qs
from apps.bot_user.schema import ListBotUserSchema, RequestBotUserSchema, ResponseBotUserSchema, UpdateBotUserSchema, GetBotUserSchema
from web.view import BaseView, require_auth


class AddView(BaseView):
    @json_schema(RequestBotUserSchema.Schema)
    @response_schema(ResponseBotUserSchema.Schema)
    @require_auth
    async def post(self):
        data = self.request['json']
        return await self.store.bot_user.add_user(data.username, data.password, data.first_name,
                                                  data.last_name,
                                                  data.subscriptions)


class ListView(BaseView):
    @response_schema(ListBotUserSchema.Schema)
    @require_auth
    async def get(self):
        data = self.request.query_string
        params = parse_qs(data)
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
