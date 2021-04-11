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
        # カテゴリ関係
        # 本当はclassにまとめた方がきっときれいだが、面倒なので順序を保ったリストをzipでまとめる
        self.keys = ["tank", "saint", "dark", "am", "rm", "lb", "dram", "sora", "luna", "other", "free", "absent"]
        self.marks = ['🛡️', '💚', '💜', '✨', '⚔', '🤖', '🐱', '☀', '🌙', '🔥', '🆓', '💤']
        self.labels = ["タンク", "支援セイント", "闇変セイント", "アーケインマスター", "ルーンマスター", "ライトブリンガー", "ドラム", "ソラリス",
                  "ルナリス", "その他火力", "フリー参加", "欠席"]

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def _update_reactions(self,msg):
        msg = await msg.channel.fetch_message(msg.id)
        embed = msg.embeds[0]
        # 何のリアクションが来たかに関わらず、addが発生したら全リアクションを更新する
        # 若干動作が遅いので、もしかしたら更新があったリアクションに絞った方がよいのかも

        # msgに紐づく全リアクションを取ってくる
        for r in msg.reactions:
            id = self.marks.index(r.emoji)
            label = "\u200b"
            # 該当リアクションに紐づくユーザのリスト
            users = await r.users().flatten()
            for u in users:
                # botでないユーザの名前を改行挟んで文字列連結
                # 本当は上のリストをうまく絞り込んでjoinするのがpythonっぽいはずだがスキル不足である
                if not u.bot:
                    label += u.name + '\n'
            embed.set_field_at(id, name=self.marks[id] + self.labels[id], value=label, inline=True)
        await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            await self._update_reactions(reaction.message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if not user.bot:
            await self._update_reactions(reaction.message)

    @commands.command()
    async def schedule_hero(self, ctx, date=""):
        # 最初の描画
        embed = discord.Embed()
        embed.title = f"タナトスヒーロー募集 ： {date} "
        for key, mark, label in zip(self.keys, self.marks, self.labels):
            embed.add_field(name=mark+label, value="\u200b", inline=True)
        msg = await ctx.send(embed=embed)
        for mark in self.marks:
            await msg.add_reaction(mark)

if __name__ == '__main__':
    bot = commands.Bot(command_prefix='/') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.add_cog(thanatos_Cog(bot))
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.run(token)
