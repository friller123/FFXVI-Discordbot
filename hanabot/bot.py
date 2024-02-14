import hikari
import arc
import os
import uvloop
import asyncio
from extension.db import *
if os.name != "nt":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  


bot = hikari.GatewayBot(os.getenv("bot_api_token"))
client = arc.GatewayClient(bot)


@client.set_startup_hook
async def startup_hook(client: arc.GatewayClient) -> None:
    db.create_tables({serverdata,botdata})

client.load_extension("extension.Timers")
client.load_extension("extension.tasks")

bot.run()