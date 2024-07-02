
import asyncio
import logging
import re
import sys
import bot.config as cfg

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from bot.schemas.error_strings import Errors
from pydantic import ValidationError

from bot.utils import build_product_on_page_string
from bot.service.search import get_search_position
from bot.service.wbsearch_client import WBSearchClient
from bot.schemas.string_constants import start_string, fallback_string, commands_info_string

dp = Dispatcher()
bot = Bot(token=cfg.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Ответ на команду /start"""
    await message.answer(start_string)

@dp.message(Command("search"))
async def command_search_handler(message: Message, command: CommandObject) -> None:
    """Ответ на команду /search"""
       
    if command.args is None:
        await message.answer(Errors.WRONG_INPUT)
        return
    
    try:
        args = command.args.split()
        if len(args) < 2:
            await message.answer(Errors.WRONG_INPUT)
            return
        
        query, item_id = " ".join(args[:-1]), args[-1]
        if not item_id.isnumeric():
            await message.answer(Errors.WRONG_INPUT_VERBOSE)
            return
        item_id = int(item_id)
            
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        product_on_page = await get_search_position(query=query, item_id=item_id, client=wb_search_client)
        if not product_on_page:
            await message.answer(Errors.ITEM_NOT_FOUND)
            return
        
    except ValidationError:
        await message.answer(Errors.WRONG_INPUT_VERBOSE)
        return
    except ValueError as e:
        await message.answer(str(e))
        return
    except Exception as e:
        await message.answer(Errors.GENERAL)
        print(repr(e))
        return
    
    await message.answer(build_product_on_page_string(product_on_page)) 

@dp.message(Command("help"))
async def command_rate_handler(message: Message) -> None:
    """Выводит список команд"""
    await message.answer(commands_info_string)
        
    
@dp.message(Command(re.compile(r"^.+$")))
async def command_fallback(message: Message) -> None:
    """Fallback для неиизвестных команд. Функция всегда должна находиться последней."""
    await message.answer(fallback_string)

 
async def main() -> None:
    async with ClientSession() as session:
        global wb_search_client # для повторного использования сессии
        wb_search_client = WBSearchClient(session=session)
        await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())