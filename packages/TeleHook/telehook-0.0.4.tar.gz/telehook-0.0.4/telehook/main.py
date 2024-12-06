

import logging
import requests
import aiohttp
import httpx
import subprocess

from fastapi import FastAPI, Request
from pyngrok import ngrok



logger = logging.getLogger('TeleHook')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TeleClient:
    def __init__(self, token=None, webhook_url=None):
        self.token = token
        self.webhook_url = webhook_url
        
        self.app = FastAPI()
        self.handlers = []
        self.setup_routes()
        self.set_webhook()

    def _setup_ngrok(self):
        tunnel = ngrok.connect(8000)
        return tunnel.public_url

    def _get_public_ip(self):
        try:
            response = httpx.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                return response.json()["ip"]
            else:
                raise Exception("Failed to get public IP")
        except Exception as e:
            raise Exception(f"Error fetching public IP: {e}")

    
    def set_webhook(self):
        print(self.webhook_url)
        url = f"https://api.telegram.org/bot{self.token}/setWebhook"
        response = httpx.post(url, data={"url": self.webhook_url})
        if response.status_code != 200:
            print(response.text)
            raise Exception("Failed to set webhook")
    
    def setup_routes(self):
        @self.app.post("/")
        async def handle_update(request: Request):
            update = await request.json()
            message = update.get('message', {})
            for handler in self.handlers:
                await handler(message)

    
    def on_message(self, filter_func):
        def decorator(func):
            async def wrapper(message):
                if filter_func(message):
                    await func(self, message)
            self.handlers.append(wrapper)
            return wrapper
        return decorator

    def run(self):
        import uvicorn
        print(self.webhook_url)
        uvicorn.run(self.app, host="0.0.0.0", port=8000)


class Filters:
    @staticmethod
    def command(cmd):
        def filter_func(message):
            text = message.get('text', '')
            return text.startswith(f"/{cmd}")
        return filter_func

    @staticmethod
    def text():
        def filter_func(message):
            return 'text' in message
        return filter_func

    @staticmethod
    def all():
        return lambda message: True
