import os
from dotenv import load_dotenv
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import Message
from gigachat import GigaChat
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
API_ID = int(os.getenv('TgApiID'))
API_HASH = str(os.getenv('TgApiHash'))
BOT_TOKEN = str(os.getenv('TgToken'))

class SimpleDB():
    def __init__(self):
        self.simple_db = dict()
    
    def add(self, key, value):
        self.simple_db = self.simple_db | {key: value}
    
    async def get(self, key: str):
        return self.simple_db[key]
    
    async def clean(self):
        self.simple_db = dict()

    def keys(self):
        return self.simple_db.keys()
    
    def stringificate(self) -> str:
        result = str()
        i = 0
        for i in range(0, len(self.simple_db)-1):
            result += f'{i}: {self.simple_db[i]}\n'
            i += 1
        return result
        

async def main():
    client = TelegramClient('bot', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    global dbs 
    dbs = SimpleDB()

    @client.on(events.NewMessage(pattern='/start'))
    async def handle_start(event: Message):
        keys = dbs.keys()
        if event.chat_id not in keys:
            dbs.add(key=event.chat_id, value=SimpleDB())
        sender = await event.get_sender()
        logger.info(f'Sender ID: {sender.id}')
        await event.respond('Это бот-суммаризатор, реализация проекта-победителя технологического трека ВСОШпП на коленке за полчаса от обиженного непрошедшего финалиста из команды 52 классического трека')

    @client.on(events.NewMessage(pattern='/shootdown'))
    async def backdoor(event: Message):
        await event.respond('Вы заебашили сервак')
        await quit(0)

    @client.on(events.NewMessage())
    async def saving_everything(event: Message, dbs=dbs):
        keys = dbs.keys()
        if event.chat_id not in keys:
            dbs.add(key=event.chat_id, value=SimpleDB())
        cur_db = await dbs.get(event.chat_id)
        cur_db.add(key=(await event.get_sender()).username, value = event.text) 
        logger.info(f'dbs: {str(dbs)} full db: {str(dbs.get(event.chat_id))}')
        

    @client.on(events.NewMessage(pattern=r'/summ (\d+)'))
    async def handle_summarize(event: Message):
        chat_id = event.chat_id

        logger.info(f'chat_id: {chat_id}')

        n = int(event.pattern_match.group(1))
        
        logger.info(f'n: {n}')

        history = await dbs.get(event.chat_id)

        logger.info(f'history: {history.stringificate()}')

        #ans = f'Я -бот. Мне надо пересказать вот такой диалог (переписку) из книги, опираюсь только на диалог (), который я дал ниже, не выдумыва, не добавляя ничего от себя: {str(history)}. Перескажи его кратко и без вступления, от лица бота, который помогает им пересказать длинную переписку. Не выдумывай, бери все только из приведенного выше диалога, это должен быть очень краткий суммаризированный пересказ '
        ans = f'Повтори мне то, что я сейчас напишу. {history.stringificate()}'

        logger.info(f'ans: {ans}')

        with GigaChat(credentials=os.getenv("GigaChatAuthKey"), verify_ssl_certs=False) as giga:
            response = giga.chat(ans)
            logger.info(f'response: {response.choices[0].message.content}')
            await event.respond(response.choices[0].message.content)

    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        quit(0)