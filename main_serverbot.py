import os

import openai
from discord import Client, Intents


class PmbBFFBot(Client):
    def __init__(self):
        self.discord_bot_token = os.environ.get("DISCORD_API_TOKEN")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        super().__init__(intents=Intents.all())
        self.run_bot()

    async def on_message(self, message):
        if message.author == self.user:
            return
        response = self.openai_response(message.content)
        await message.channel.send(response)

    def openai_response(self, message: str) -> str:
        openai.api_key = self.openai_api_key
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        if response.get("choices"):
            return response.get("choices")[0]["text"]

    def run_bot(self):
        super().run(self.discord_bot_token)


if __name__ == "__main__":
    bot = PmbBFFBot()
