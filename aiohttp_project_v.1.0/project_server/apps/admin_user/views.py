from aiohttp import web
from aiohttp_apispec import json_schema, response_schema

from apps.admin_user.schema import ResponseSchema, LoginSchema, RequestSchema
from web.view import BaseView, require_auth


class AdminLoginView(BaseView):
    @json_schema(LoginSchema.Schema)
    @response_schema(ResponseSchema.Schema)
    async def post(self):
        data = self.request["json"]
        user = await self.store.admin.login(data.username, data.password)
        session = await self.store.session.generate_session(user.username)
        response = web.json_response({"data": ResponseSchema.Schema().dump(user)})
        response.set_cookie("session_id", session.id)
        return response


class AdminAddUserView(BaseView):
    @json_schema(RequestSchema.Schema)
    @response_schema(ResponseSchema.Schema)
    @require_auth
    async def post(self):
        data = self.request["json"]
        return await self.store.admin.add_user(
            data.username, data.password, data.first_name, data.last_name
        )
