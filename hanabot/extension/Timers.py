import hikari
import arc
from extension.db import *
from extension.calander import *
import datetime
import os

plugin = arc.GatewayPlugin("Timers")

if os.getenv("guildIDs") == "":
    own_guild=hikari.UNDEFINED
else:
    own_guild = [int(i) for i in os.getenv("guildIDs").split(",")]

configcommands = plugin.include_slash_group("config","Commands for setting up and editing the timer",guilds=own_guild)


async def create_initial_message(channel :int,guildID :int) -> None:
    data = serverdata.select().where((serverdata.ChannelID == channel) & (serverdata.ServerID == guildID)).get()
    entries = await getdates(data.Entries)
    currenttime = datetime.datetime.now()
    currenttime = int(currenttime.timestamp())
    formatedsrting = "\n".join(entries)+"\n"+"\n"+f"last refesh: <t:{str(currenttime)}:R>"
    if data.MessageID == None:
        Message = await plugin.client.rest.create_message(channel,formatedsrting)
        serverdata.update({serverdata.MessageID: Message.id}).where((serverdata.ChannelID == channel) & (serverdata.ServerID == guildID)).execute()
    else:
        return


@configcommands.include
@arc.slash_subcommand("setup-autotimers", "Setup channel and how often it should refresh")
async def setup_autoimers(
    ctx: arc.GatewayContext,
    channel: arc.Option[hikari.TextableGuildChannel, arc.ChannelParams("channel to setup")],
    numdates: arc.Option[int, arc.IntParams("How many dates should be fetched")]
):
    guildID = ctx.guild_id
    if not os.path.exists(".data/token.pickle"):
        await ctx.respond("token.pickle not found run the init-ca.py then run the bot and this command again",flags=hikari.MessageFlag.EPHEMERAL)
        return
    await ctx.respond("working ...", flags=hikari.MessageFlag.EPHEMERAL)
    if numdates == 0:
        await ctx.respond("You cant check 0 entries :>", flags=hikari.MessageFlag.EPHEMERAL)
        return
    result = serverdata.select().where((serverdata.ChannelID == channel.id) & (serverdata.ServerID == guildID))   
    if result.exists():
        result = result.get()
        if result.MessageID == None:
            await create_initial_message(channel.id,guildID)
            await ctx.respond("Done", flags=hikari.MessageFlag.EPHEMERAL)
            return
        await ctx.respond("ChannelID already exists", flags=hikari.MessageFlag.EPHEMERAL)
        return
    else:
        data = serverdata(ChannelID = channel.id, ServerID = guildID, MessageID = None, Entries = numdates)  
        data.save()
        await create_initial_message(channel.id,guildID)
    await ctx.respond("Done", flags=hikari.MessageFlag.EPHEMERAL)

@configcommands.include
@arc.slash_subcommand("change-dates", "Change how many dates should be fetched")
async def change_dates(
    ctx: arc.GatewayContext,
    channel: arc.Option[hikari.TextableChannel, arc.ChannelParams("which channel to change")],
    numdates: arc.Option[int, arc.IntParams("How many dates should be fetched"),]
):
    guildID = ctx.guild_id
    if numdates == 0:
        await ctx.respond("You cant check 0 entries :>", flags=hikari.MessageFlag.EPHEMERAL)
        return
    result = serverdata.select().where((serverdata.ChannelID == channel.id) & (serverdata.ServerID == guildID))
    if not result.exists():
        await ctx.respond("Channel isnt setup for entries", ephemeral=True)
        return
    serverdata.update({serverdata.Entries: numdates}).where((serverdata.ChannelID == channel.id) & (serverdata.ServerID == guildID)).execute()
    await ctx.respond("Done", flags=hikari.MessageFlag.EPHEMERAL)

@configcommands.include
@arc.slash_subcommand("change-timers","Change how often the timer should refresh")
async def change_timer(
    ctx: arc.GatewayContext,
    hours: arc.Option[int, arc.IntParams("How many hours")],
    minutes: arc.Option[int, arc.IntParams("How many minutes")],
    seconds: arc.Option[int, arc.IntParams("How many seconds")]
):
    guildID = ctx.guild_id
    result = botdata.select().where((botdata.ServerID == guildID))
    if not result.exists():
        data = botdata(ServerID = guildID, Hours = hours, Minutes = minutes, Seconds = seconds)
        data.save()
        await ctx.respond("Done", flags=hikari.MessageFlag.EPHEMERAL)
        return
    botdata.update({botdata.Hours: hours, botdata.Minutes: minutes, botdata.Seconds: seconds}).where((botdata.ServerID == guildID)).execute()
    await ctx.respond("Done", flags=hikari.MessageFlag.EPHEMERAL)


@arc.loader
def loader(client : arc.GatewayClient) -> None:
    client.add_plugin(plugin)
    
@arc.unloader
def unloader(client : arc.GatewayClient) -> None:
    client.remove_plugin(plugin)