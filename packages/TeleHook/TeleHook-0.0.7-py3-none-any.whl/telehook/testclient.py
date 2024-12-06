from flask import Flask, request
import requests

class testclient:
    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.app = Flask(__name__)
        self.client_id = None
        self.raw_handler = None
        self.base_url = f'https://api.telegram.org/bot{self.token}'

        # Set the webhook when initializing
        self.set_webhook()

        # Setup the Flask route for handling updates
        self.app.add_url_rule('/webhook', 'webhook', self.handle_update, methods=['POST'])

    def set_webhook(self):
        response = requests.post(
            f'{self.base_url}/setWebhook',
            data={'url': self.url}
        )
        if response.status_code == 200:
            print('Webhook set successfully!')
            self.client_id = response.json().get('result', {}).get('id')
        else:
            print('Failed to set webhook.')

    def on_raw(self):
        def decorator(func):
            self.raw_handler = func
            return func
        return decorator

    def handle_update(self):
        update = request.json
        if self.raw_handler:
            self.raw_handler(self.client_id, update)
        return 'OK'

    def run(self):
        self.app.run()

"""
# Example usage
if __name__ == '__main__':
    app = TeleHook(token='YOUR_BOT_TOKEN', url='https://your-server-url.com/webhook')

    @app.on_raw()
    async def get_raw_update(client, message):
        print(f"Client ID: {client}")
        print("Message:", message)

    app.run()

"""
  
