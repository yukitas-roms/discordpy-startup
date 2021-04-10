import discord
from discord.ext import commands
import os
import traceback

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
    # 残り人数カウンター
    cnt = 12

    # カテゴリ関係
    # 本当はclassにまとめた方がきっときれい
    # 面倒なので順序を保ったリストをzipでまとめる
    keys = ["tank", "saint", "dark", "am", "rm", "lb", "dram", "sora","luna", "other", "free", "absent"]
    marks = ['🛡️', '💚', '💜', '✨', '⚔', '🤖', '🐱', '☀', '🌙', '🔥', '🆓', '💤']
    labels = ["タンク", "支援セイント", "闇変セイント", "アーケインマスター", "ルーンマスター", "ライトブリンガー", "ドラム", "ソラリス",
              "ルナリス", "その他火力", "フリー参加", "欠席"]

    # 最初の描画
    msg_frame = discord.Embed(title=f"タナトスヒーロー募集 {date} ＠ {cnt} 人", colour=0x1e90ff)
    for key, mark, label in zip(keys, marks, labels):
        msg_frame.add_field(name=mark+label, value="\u200b", inline=True)
    msg = await ctx.send(embed=msg_frame)
    for mark in marks:
        await msg.add_reaction(mark)

bot.run(token)
