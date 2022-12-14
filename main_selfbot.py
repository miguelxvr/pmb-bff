import os
from time import sleep
from dotenv import load_dotenv

import discum
import openai

load_dotenv()

FIXED_PROMPT = "Siga as instruções a seguir na construção das respostas: Inclua abreviações e siglas utilizadas na comunicação na internet na elaboração das respostas. Remova todos os acentos. Utilize a palavra Liiixo! sempre que aplicável. Utilize pouco a vírgula. Responda com no máximo 20 caracteres. Portanto, responda a pergunta: "
DISCORD_USER_TOKEN = os.environ.get("DISCORD_USER_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = discum.Client(token=DISCORD_USER_TOKEN)


class PmbBFFBot(object):
    username: str
    discriminator: str

    @staticmethod
    @bot.gateway.command
    def on_message(resp):
        if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
            user = bot.gateway.session.user
            PmbBFFBot.username = user['username']
            PmbBFFBot.discriminator = user['discriminator']
            print("Logged in as {}#{}".format(PmbBFFBot.username, PmbBFFBot.discriminator))
        if resp.event.message:
            message = resp.parsed.auto()
            guildID = message['guild_id'] if 'guild_id' in message else None  # because DMs are technically channels too
            channelID = message['channel_id']
            username = message['author']['username']
            discriminator = message['author']['discriminator']
            content = message['content']
            if username == PmbBFFBot.username:
                return
            print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))
            prompt = FIXED_PROMPT + content
            print(prompt)
            response = PmbBFFBot.openai_response(prompt)
            sleep(10)
            bot.sendMessage(channelID, response)

    @staticmethod
    def openai_response(message: str) -> str:
        openai.api_key = OPENAI_API_KEY
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

    @staticmethod
    def run_bot():
        bot.gateway.run()


if __name__ == "__main__":
    PmbBFFBot.run_bot()
