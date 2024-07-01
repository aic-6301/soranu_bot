# いちこめらんきんぐの集計中及び処理開始を始めて再読み込み、再起動を行うといちこめらんきんぐが正常に完了しません。
import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, time, timedelta



class onecomment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.ranking.start()
        self.embed = None
        self.data = {}
        self.enable = True

    def is_time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.channel == self.bot.get_channel(867692303664807946):
            if message.author.bot:
                return
            if message.author.id in self.messages:
                # print("added")
                return
            msg_time = message.created_at + timedelta(hours=9)
            if self.is_time_in_range(time(23, 59), time(0, 1), msg_time.time()):
                self.messages[message.author.id] = (message.author.id, (message.created_at + timedelta(hours=9)).strftime('%H%M%S%f'), message.id)
            else:
                # print("not time")
                return

    @tasks.loop()
    async def ranking(self):
        channel = self.bot.get_channel(867692303664807946)
        now = datetime.now()
        if now.strftime("%H:%M") == "00:01":
            if self.enable is True:
                if self.embed is None:
                    try:
                        sorted_messages = sorted(self.messages.items(), key=lambda x: abs(int(x[1][1])))
                        rank_message = "> 0:00に一番近く送ったメッセージランキング\n"
                        for i, msg in enumerate(sorted_messages):
                            rank_message += f"{i+1}位. <@{msg[1][0]}> 送信時間:{msg[1][1][:2]}:{msg[1][1][2:4]}:{msg[1][1][4:6]}.{msg[1][1][6:]} [Link](https://discord.com/channels/867677146260439050/867692303664807946/{msg[1][2]})\n"
                        self.embed = await channel.send(embed=discord.Embed(title="一コメランキング", description=rank_message, timestamp=now,color=discord.Color.blue()
                                                                            ).set_footer(text="この機能はβ版です。不具合等あればあいしぃーまで。" ))
                        self.messages = {}
                    except Exception as e:
                        self.embed = await channel.send(content="<@964887498436276305>", embed=discord.Embed(title="エラー", description=f"送信する際にエラーが発生しました。\nエラー内容：`{e}`", color=discord.Color.red()))
            else:
                self.enable = True
                self.embed = "なんかいれとけ"
        elif now.strftime("%H:%M") == "23:59":
            if self.enable is True:
                if self.embed is None:
                    self.embed = await channel.send(content="<@&1224736836744908893> 寝る時間です。ついでに１コメも。",embed=discord.Embed(title="一コメランキング", description=f"計測中...結果は{discord.utils.format_dt((now+timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0))}に送信されます。", color=discord.Color.blue()))
        else:
            self.embed = None

    group = app_commands.Group(name="onecomment", description="一コメ関連")
    
    @group.command(name="stop", description="今日の一コメだけ無効化します")
    @app_commands.default_permissions(manage_guild=True)
    async def stop(self, interaction:discord.Interaction, reason:str):
        if self.enable is True:
            self.enable = False
            await interaction.response.send_message(embed=discord.Embed(title="無効化", description=f"今日の一コメを中止しました。\n理由:{reason}", color=discord.Color.red()), ephemeral=True)
            await self.bot.get_channel(867692303664807946).send(content="<@&1224736836744908893>", embed=discord.Embed(title="一コメランキング", description=f"管理者が今日の一コメを無効化しました。\n理由:{reason}", color=discord.Color.orange()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="無効化", description="今日の一コメは既に無効化されています。", color=discord.Color.red()), ephemeral=True)

    @group.command(name="start", description="今日の一コメだけ有効化します")
    @app_commands.default_permissions(manage_guild=True)
    async def start(self, interaction:discord.Interaction):
        if self.enable is False:
            self.enable = True
            await interaction.response.send_message(embed=discord.Embed(title="有効化", description="今日の一コメを有効化にしました", color=discord.Color.red()), ephemeral=True)
            await self.bot.get_channel(867692303664807946).send(content="<@&1224736836744908893>", embed=discord.Embed(title="一コメランキング", description="管理者が今日の一コメを有効化にしました。", color=discord.Color.green()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="有効化", description="今日の一コメは既に有効化されています。", color=discord.Color.red()), ephemeral=True)

    async def cog_unload(self):
        self.ranking.stop()
        

async def setup(bot: commands.Bot):
    await bot.add_cog(onecomment(bot))