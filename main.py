from Kyasher import Kyash
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

aaaid = 123456789 # 送金リンクを作れるユーザー
TOKEN = 'とーくん' # botのtoken
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

# はじめは下の6行の＃を外して実行してそれ以降は実行しなくて大丈夫（＃をつけて大丈夫）

#kyash=Kyash("メールアドレス","パスワード",proxy=None) # メアドとパスワードを入力
#otp=input("OTP? :")#SMSに届いた6桁の認証番号
#kyash.login(otp)
#print(f'トークンは{kyash.access_token}')#有効期限は1ヶ月
#print(kyash.client_uuid) #ぶっちゃけいらんかも
#print(kyash.installation_uuid) #ぶっちゃけいらんかも

# 二回目以降は下のtokenを入力して＃を外して上のコードを削除か＃をつける

#kyash=Kyash(access_token="とーくん") # はじめに実行したときにでてきたkyashのtokenを入力
@bot.tree.command(name="zandaka", description="俺のkyash残高をげっと")
async def zandaka(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)  # 応答遅延でタイムアウト回避
    kyash.get_wallet()
    残高 = (kyash.all_balance)
    await interaction.followup.send(f'{残高}円', ephemeral=True)

@bot.tree.command(name="kakutoku", description="kyashリンクを獲得")
async def kakutoku(interaction: discord.Interaction, link: str):
    await interaction.response.defer(thinking=True)  # 応答遅延でタイムアウト回避
    link_info=kyash.link_check(link)
    embed = discord.Embed(
            title="link獲得！",
            description="kyashだ！",
            color=discord.Color.blue()
        )
    embed.add_field(name="誰から:", value=kyash.link_sender_name, inline=False)
    embed.add_field(name="何円:", value=(kyash.link_amount), inline=False)
    await interaction.followup.send(embed = embed, ephemeral=True)
    uuid = kyash.link_uuid
    
    kyash.link_recieve(url=link,link_uuid=uuid)
    await interaction.channel.send('受取完了')

@bot.tree.command(name="kakunin", description="kyashリンクを確認")
async def kakunin(interaction: discord.Interaction, link: str):
    await interaction.response.defer(thinking=True)  # 応答遅延でタイムアウト回避
    link_info=kyash.link_check(link)
    embed = discord.Embed(
            title="link獲得！",
            description="kyashだ！",
            color=discord.Color.blue()
        )
    embed.add_field(name="誰から:", value=kyash.link_sender_name, inline=False)
    embed.add_field(name="何円:", value=(kyash.link_amount), inline=False)
    await interaction.followup.send(embed = embed, ephemeral=True)

@bot.tree.command(name="seikyuu", description="kyash請求リンクを作成")
async def seikyuu(interaction: discord.Interaction, amount: int,message : str):
    await interaction.response.defer(thinking=True)
    kyash.create_link(amount=amount,message=message,is_claim=True)
    await interaction.followup.send('kyash.created_link', ephemeral=True)

@bot.tree.command(name="soukin", description="kyash送金リンクを作成")
async def soukin(interaction: discord.Interaction, amount: int,message : str):
    await interaction.response.defer(thinking=True)
    if interaction.user.id == aaaid :
        kyash.create_link(amount=amount,message=message,is_claim=False)
        await interaction.followup.send(kyash.created_link, ephemeral=False)
    else:
        await interaction.followup.send('あなたは実行できません', ephemeral=False)
bot.run(TOKEN)
