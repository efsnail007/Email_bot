from .http_client import HTTPClient


class BackendAPIClient:
    def __init__(self, client: HTTPClient):
        self.client = client

    async def get_user(self, tg_id: str):
        path = f"/api/user/{tg_id}/"
        return await self.client.get(path)

    async def create_user(self, tg_id: str, first_name: str, last_name: str):
        path = f"/api/user/"
        data = {"tg_id": tg_id, "first_name": first_name, "last_name": last_name}
        return await self.client.post(path, data=data)

    async def create_email(self, tg_id: str, login: str, password: str):
        path = f"/api/user/{tg_id}/email/"
        data = {"email": login, "password": password}
        return await self.client.post(path, data=data)

    async def get_list_email(self, tg_id: str):
        path = f"/api/user/{tg_id}/email/"
        return await self.client.get(path)
