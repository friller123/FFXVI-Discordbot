import hikari
import arc
import asyncio
from extension.db import *
from extension.calander import getdates
from datetime import datetime
import os

plugin = arc.GatewayPlugin("Tasks")

if os.getenv("guildIDs") == "":
    own_guild=hikari.UNDEFINED
else:
    own_guild = [int(i) for i in os.getenv("guildIDs").split(",")]

timer = plugin.include_slash_group("timer","Command for changing the timer for this server",guilds=own_guild)

async def refreshloop(guild):
    while True:
        await plugin.client.rest.fetch_guild(guild)
        timedata = botdata.select().where(botdata.ServerID == guild.id)
        if not timedata.exists():
            print("no time data")
            return 
        timedata = timedata.get()
        await asyncio.sleep(timedata.Hours * 3600 + timedata.Minutes * 60 + timedata.Seconds)
        data = serverdata.select().where(serverdata.ServerID == guild.id)
        if data.exists():
            for entry in data:
                entries = await getdates(entry.Entries)
                currenttime = datetime.now()
                currenttime = int(currenttime.timestamp())
                formatedsrting = "\n".join(entries)+"\n"+"\n"+f"last refesh: <t:{str(currenttime)}:R>"
                await plugin.client.rest.edit_message(entry.ChannelID,entry.MessageID,formatedsrting)   
        else:
            print("how did we get here")


@timer.include
@arc.slash_subcommand("start","start a timer")
async def change_timer(
    ctx: arc.GatewayContext,
):
    guild = ctx.get_guild()
    try:
        task, = [task for task in asyncio.all_tasks() if task.get_name() == f"{guild.id}"]
        await ctx.respond(f"Timer already running", flags=hikari.MessageFlag.EPHEMERAL)
        return
    except:
        loop = asyncio.get_event_loop()
        loop.create_task(refreshloop(guild),name=f"{guild.id}")
        loop = asyncio.all_tasks()
        await ctx.respond(f"Timer refesh started for this server", flags=hikari.MessageFlag.EPHEMERAL)

@timer.include
@arc.slash_subcommand("stop","stop the current running timer")
async def stop_timer(
    ctx: arc.GatewayContext
):   
    guild = ctx.get_guild()
    try:
        task, = [task for task in asyncio.all_tasks() if task.get_name() == f"{guild.id}"]
        task.cancel()
        await ctx.respond(f"Timer stoppped for this server", flags=hikari.MessageFlag.EPHEMERAL)
        return
    except:
        await ctx.respond(f"Timer not running for this server", flags=hikari.MessageFlag.EPHEMERAL)
        return

@timer.include
@arc.slash_subcommand("check","check if a timer is running")
async def check_timer(
    ctx: arc.GatewayContext
):   
    guild = ctx.get_guild()
    try:
        task, = [task for task in asyncio.all_tasks() if task.get_name() == f"{guild.id}"]
        await ctx.respond("Timer is running for this server", flags=hikari.MessageFlag.EPHEMERAL)
        return
    except:
        await ctx.respond(f"Timer not running for this server", flags=hikari.MessageFlag.EPHEMERAL)
        return

@arc.loader
def loader(client : arc.GatewayClient) -> None:  
    client.add_plugin(plugin)
    
@arc.unloader
def unloader(client : arc.GatewayClient) -> None:
    client.remove_plugin(plugin)