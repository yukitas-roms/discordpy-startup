from discord.ext import commands
import os
import traceback
import discode

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

    
@bot.command()
async def schedule_hero(ctx, date=""):
    cnt = 12
    tank_name = ""
    saint_name = ""
    msg_frame = discord.Embed(title=f"タナトスヒーロー募集 {date}", colour=0x1e90ff)
    msg_frame.add_field(name=f"あと{cnt}人 募集中\n", value=None, inline=True)
    msg_frame.add_field(name=f"🟥タンク：{tank_name} \n", value=None, inline=True)
    msg_frame.add_field(name=f"🟩支援セイント：{saint_name}\n", value=None, inline=True)
    msg_frame.add_field(name=f"🟦アーケインマスター：\n", value=None, inline=True)
    msg_frame.add_field(name=f"🔴ルーンマスター : \n", value=None, inline=True)
    msg = await ctx.send(embed=msg_frame)
    await msg.add_reaction('🟥')
    await msg.add_reaction('🟩')
    await msg.add_reaction('🟦')
    await msg.add_reaction('🔴')
bot.run(token)
