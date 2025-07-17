import asyncio
import httpx

async def test_login():
    async with httpx.AsyncClient() as client:
        data = {"username": "admin1", "password": "admin"}
        response = await client.post("http://127.0.0.1:8000/auth/login", data=data)
        print(response.status_code)
        print(response.json())

asyncio.run(test_login())
