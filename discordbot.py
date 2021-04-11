import discord
from discord.ext import commands
import os
import traceback

#@commands.event
#async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)

# classにまとめます
class thanatos_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.embed = discord.Embed(title="", color=0x1e90ff)
        self.msg = None
        # 残り人数カウンター
        self.cnt = 12
        self.date = ""
        # カテゴリ関係
        # 本当はclassにまとめた方がきっときれいだが、面倒なので順序を保ったリストをzipでまとめる
        self.keys = ["tank", "saint", "dark", "am", "rm", "lb", "dram", "sora", "luna", "other", "free", "absent"]
        self.marks = ['🛡️', '💚', '💜', '✨', '⚔', '🤖', '🐱', '☀', '🌙', '🔥', '🆓', '💤']
        self.labels = ["タンク", "支援セイント", "闇変セイント", "アーケインマスター", "ルーンマスター", "ライトブリンガー", "ドラム", "ソラリス",
                  "ルナリス", "その他火力", "フリー参加", "欠席"]

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            self.cnt -= 1
            id = self.marks.index(reaction.emoji)
            self.embed.set_field_at(id, name=self.marks[id]+self.labels[id], value=user, inline=True)
            print(self.embed.fields[id])
            await self.msg.edit(embed=self.embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if not user.bot:
            print(reaction, user)

    @commands.command()
    async def schedule_hero(self, ctx, date=""):
        # 最初の描画
        self.date = date
        self.embed.title = f"タナトスヒーロー募集 {self.date} ＠ {self.cnt} 人"
        for key, mark, label in zip(self.keys, self.marks, self.labels):
            self.embed.add_field(name=mark+label, value="\u200b", inline=True)
        self.msg = await ctx.send(embed=self.embed)
        for mark in self.marks:
            await self.msg.add_reaction(mark)


if __name__ == '__main__':
    bot = commands.Bot(command_prefix='/') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.add_cog(thanatos_Cog(bot))
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.run(token)
