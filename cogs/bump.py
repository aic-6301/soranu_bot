import datetime
import requests
import asyncio
import time
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont

class bump(commands.Cog):
    def __init__(self):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(message):
    
    
      if message.author.bot:
    
          if message.embeds:
            for embed in message.embeds:
                title = embed.title
                description = embed.description
                
                if title == "DISBOARD: Discordサーバー掲示板" or description == "表示順をアップしたよ":
    
                  current_time = int(time.time())
                  two_hours_later = current_time + 7200
    
    
                  IMAGE_SIZE = (1200, 600)
                  TEXT_COLOR = (255, 255, 255)
                  FONT_PATH = "NotoSerifJP-Bold.otf"
    
                  guild = client.get_guild(SERVER ID)
    
                  server_icon_url = str(guild.icon.url)
                  server_icon = Image.open(requests.get(server_icon_url, stream=True).raw).resize((200, 200))
    
                  img = Image.new('RGB', IMAGE_SIZE, (162, 225, 249))
                  draw = ImageDraw.Draw(img)
    
                  font = ImageFont.truetype(FONT_PATH, 60)
                  small_font = ImageFont.truetype(FONT_PATH, 40)
    
                  draw.text((20, 20), "BUMPを検知!", fill=TEXT_COLOR, font=font)
                  current_time = datetime.datetime.now().strftime('%H:%M')
                  draw.text((1030, 20), current_time, fill=TEXT_COLOR, font=font)
                  
                  img.paste(server_icon, (20, 350))
    
                  future_time = (datetime.datetime.now() + timedelta(hours=2)).strftime('%Y年%m月%d日 %H:%M')
                  draw.text((250, 460), f"{future_time} (2時間後) に通知します！", fill=TEXT_COLOR, font=small_font)
                  draw.text((250, 500), "Bumpありがとう! またBumpしてね!", fill=TEXT_COLOR, font=small_font)
    
                  img_path = 'bump_image.png'
                  img.save(img_path)
    
                  with open(img_path, 'rb') as f:
                      file = discord.File(f)
    
                      embed = discord.Embed(
                        title="bumpを検知しました!",
                        color=COLOR,
                        description="bumpしてくれてありがとうございます!\n"+
                                   f"<t:{two_hours_later}:f> (<t:{two_hours_later}:R>) に通知します!",
                        timestamp=message.created_at
                      )
                      embed.set_author(name="この画像生成はまだβ版のため不具合が発生する可能性があります",
                                      icon_url=message.guild.icon
                      )
                      embed.set_image(url=f"attachment://{img_path}")
                      await message.channel.send(embed=embed, file=file)
                      
                      await asyncio.sleep(7200)
    
                      await message.channel.send("<@&METION ROLE> ")
                      embed = discord.Embed(
                        title="bumpの時間です!",
                        color=COLOR,
                        description=f"`/bump`して{guild.name} を活発化させよう!",
                      )
                      await message.channel.send(embed=embed)
                      
          return
async def setup(bot) -> None:
    await bot.add_cog(bump(bot))
