import json
import discord
from discord import app_commands
from discord.ext import commands
from discord import Object
import os

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("エラー: 環境変数 DISCORD_BOT_TOKEN が設定されていません。")
    exit(1)

# intentsを設定（全部有効化）
intents = discord.Intents.all()

# Botのインスタンス作成
bot = commands.Bot(command_prefix="!", intents=intents)

SOURCE_CHANNEL_ID = 1353362211694706749

# 許可ロールの管理
allowed_roles = {}

def load_allowed_roles():
    try:
        with open("allowed_roles.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return {}

def save_allowed_roles():
    with open("allowed_roles.json", "w") as f:
        json.dump(allowed_roles, f, indent=4)

# アナウンスチャンネルの管理
announcement_channels = {}

def load_announcement_channels():
    try:
        with open("announcement_channels.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return {}

def save_announcement_channels():
    with open("announcement_channels.json", "w") as f:
        json.dump(announcement_channels, f, indent=4)

async def check_permissions(interaction: discord.Interaction):
  try:
      if not interaction.guild:
          return False

      member = await interaction.guild.fetch_member(interaction.user.id)
      if member and member.guild_permissions.administrator:
          return True  # 管理者であれば許可

      guild_id = str(interaction.guild_id)
      if guild_id not in allowed_roles:
          return False

      user_roles = [role.id for role in member.roles]
      allowed = allowed_roles.get(guild_id, [])
      return any(role_id in allowed for role_id in user_roles)  # 許可ロールに所属しているかチェック
  except Exception as e:
      print(f"権限チェックエラー: {e}")
      return False

FORWARD_MAP_FILE = "forward_map.json"

def load_forward_map():
    if os.path.exists(FORWARD_MAP_FILE):
        with open(FORWARD_MAP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_forward_map(data):
    with open(FORWARD_MAP_FILE, "w") as f:
        json.dump(data, f, indent=2)

forward_map = load_forward_map()

@bot.event
async def on_ready():
    global allowed_roles, announcement_channels
    allowed_roles = load_allowed_roles()
    announcement_channels = load_announcement_channels()
    try:
        await bot.tree.sync()
        print("コマンドを同期しました")
    except Exception as e:
        print(f"コマンドの同期に失敗: {e}")
    print(f"{bot.user} としてログインしました")

# ホワイトリスト管理コマンド
@bot.tree.command(name="add_whitelist", description="コマンド許可ロールを追加します")
@app_commands.describe(role="許可するロール")
async def add_whitelist(interaction: discord.Interaction, role: discord.Role):
    try:
        if not interaction.guild:
            await interaction.response.send_message("このコマンドはサーバー内でのみ使用できます", ephemeral=True)
            return
            
        member = interaction.guild.get_member(interaction.user.id)
        if not member:
            member = await interaction.guild.fetch_member(interaction.user.id)
            
        if not member or not member.guild_permissions.administrator:
            await interaction.response.send_message("このコマンドは管理者のみが使用できます", ephemeral=True)
            return
    except discord.NotFound:
        await interaction.response.send_message("ユーザーが見つかりません", ephemeral=True)
        return
    except Exception as e:
        await interaction.response.send_message("権限の確認中にエラーが発生しました", ephemeral=True)
        print(f"権限チェックエラー: {e}")
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in allowed_roles:
        allowed_roles[guild_id] = []

    if role.id not in allowed_roles[guild_id]:
        allowed_roles[guild_id].append(role.id)
        save_allowed_roles()
        await interaction.response.send_message(f"{role.name} を許可ロールに追加しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{role.name} は既に許可ロールです", ephemeral=True)

@bot.tree.command(name="delete_whitelist", description="許可ロールを削除します")
@app_commands.describe(role="削除するロール")
async def delete_whitelist(interaction: discord.Interaction, role: discord.Role):
    try:
        member = await interaction.guild.fetch_member(interaction.user.id)
        if not member.guild_permissions.administrator:
            await interaction.response.send_message("このコマンドは管理者のみが使用できます", ephemeral=True)
            return
    except Exception as e:
        await interaction.response.send_message("権限の確認中にエラーが発生しました", ephemeral=True)
        print(f"権限チェックエラー: {e}")
        return

    guild_id = str(interaction.guild_id)
    if guild_id in allowed_roles and role.id in allowed_roles[guild_id]:
        allowed_roles[guild_id].remove(role.id)
        save_allowed_roles()
        await interaction.response.send_message(f"{role.name} を許可ロールから削除しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{role.name} は許可ロールではありません", ephemeral=True)

@bot.tree.command(name="show_whitelist", description="許可ロールを表示します")
async def show_whitelist(interaction: discord.Interaction):
    try:
        member = await interaction.guild.fetch_member(interaction.user.id)
        if not member.guild_permissions.administrator:
            await interaction.response.send_message("このコマンドは管理者のみが使用できます", ephemeral=True)
            return
    except Exception as e:
        await interaction.response.send_message("権限の確認中にエラーが発生しました", ephemeral=True)
        print(f"権限チェックエラー: {e}")
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in allowed_roles or not allowed_roles[guild_id]:
        await interaction.response.send_message("許可ロールは設定されていません", ephemeral=True)
        return

    roles = [f"<@&{role_id}>" for role_id in allowed_roles[guild_id]]
    await interaction.response.send_message("許可ロール:\n" + "\n".join(roles), ephemeral=True)

# アナウンスチャンネル管理コマンド
@bot.tree.command(name="add_announcement_list", description="アナウンスチャンネルを追加します")
@app_commands.describe(channel="追加するチャンネル")
async def add_announcement_list(interaction: discord.Interaction, channel: discord.TextChannel):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in announcement_channels:
        announcement_channels[guild_id] = []

    if channel.id not in announcement_channels[guild_id]:
        announcement_channels[guild_id].append(channel.id)
        save_announcement_channels()
        await interaction.response.send_message(f"{channel.mention} をアナウンスチャンネルに追加しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} は既にアナウンスチャンネルです", ephemeral=True)

@bot.tree.command(name="announcement_list", description="アナウンスチャンネルを表示します")
async def announcement_list(interaction: discord.Interaction):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in announcement_channels or not announcement_channels[guild_id]:
        await interaction.response.send_message("アナウンスチャンネルは設定されていません", ephemeral=True)
        return

    channels = [f"<#{channel_id}>" for channel_id in announcement_channels[guild_id]]
    await interaction.response.send_message("アナウンスチャンネル:\n" + "\n".join(channels), ephemeral=True)

@bot.tree.command(name="delete_announcement_list", description="アナウンスチャンネルを削除します")
@app_commands.describe(channel="削除するチャンネル")
async def delete_announcement_list(interaction: discord.Interaction, channel: discord.TextChannel):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id in announcement_channels and channel.id in announcement_channels[guild_id]:
        announcement_channels[guild_id].remove(channel.id)
        save_announcement_channels()
        await interaction.response.send_message(f"{channel.mention} をアナウンスチャンネルから削除しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} はアナウンスチャンネルではありません", ephemeral=True)

# その他のコマンド
@bot.tree.command(name="user_information", description="ユーザーの情報を表示します")
@app_commands.describe(user="情報を表示するユーザー")
async def user_information(interaction: discord.Interaction, user: discord.Member):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    embed = discord.Embed(title="ユーザー情報", color=user.color)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="名前", value=str(user), inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="アカウント作成日", value=user.created_at.strftime("%Y/%m/%d %H:%M:%S"), inline=True)
    embed.add_field(name="サーバー参加日", value=user.joined_at.strftime("%Y/%m/%d %H:%M:%S"), inline=True)
    embed.add_field(name="最上位ロール", value=user.top_role.mention, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="message", description="指定したチャンネルにメッセージを送信します")
@app_commands.describe(
    channel="送信先チャンネル",
    message="送信するメッセージ",
    by_user="送信者名を表示する"
)
async def message(interaction: discord.Interaction, channel: discord.TextChannel, message: str, by_user: bool = False):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    if by_user:
        message = f"by {interaction.user.mention}\n{message}"

    await channel.send(message)
    await interaction.response.send_message("メッセージを送信しました", ephemeral=True)

@bot.tree.command(name="delete_message", description="指定した数のメッセージを削除します")
@app_commands.describe(amount="削除するメッセージ数 (1-99)")
async def delete_message(interaction: discord.Interaction, amount: int):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    if not 1 <= amount <= 99:
        await interaction.response.send_message("1から99の間の数を指定してください", ephemeral=True)
        return

    try:
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("このコマンドはテキストチャンネルでのみ使用できます", ephemeral=True)
            return
            
        if not interaction.channel.permissions_for(interaction.guild.me).manage_messages:
            await interaction.response.send_message("メッセージを削除する権限がありません", ephemeral=True)
            return
            
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{len(deleted)}件のメッセージを削除しました", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("メッセージを削除する権限がありません", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"メッセージの削除中にエラーが発生しました: {e}", ephemeral=True)

@tree.command(name="CoreBot_Update", description="アップデート情報フォローチャンネルを登録・解除します")
@app_commands.describe(channel="転送先のチャンネル")
async def corebot_update(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id_str = str(interaction.guild_id)
    current = forward_map.get(guild_id_str)

    if current == channel.id:
        # 登録済みなら解除
        forward_map.pop(guild_id_str)
        save_forward_map(forward_map)
        await interaction.response.send_message(f"{channel.mention} への転送を解除しました。", ephemeral=True)
    else:
        # 新規登録または別チャンネルに変更
        forward_map[guild_id_str] = channel.id
        save_forward_map(forward_map)
        await interaction.response.send_message(f"{channel.mention} を転送先に設定しました！", ephemeral=True)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.channel.id == SOURCE_CHANNEL_ID:
        for guild_id, channel_id in forward_map.items():
            dest = bot.get_channel(channel_id)
            if dest:
                await dest.send(f"【CoreBot更新】\n{message.content}")

    await bot.process_commands(message)

@bot.tree.command(name="support", description="サポートサーバーの招待リンクを表示します")
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="サポートサーバー",
        description="サポートが必要な場合は、以下のリンクからサーバーに参加してください",
        color=discord.Color.blue()
    )
    embed.add_field(name="招待リンク", value="https://discord.gg/Yv9uJ32KkT")
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    try:
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        if guild_id in announcement_channels and message.channel.id in announcement_channels[guild_id]:
            try:
                await message.publish()
                await message.add_reaction("✅")
                await message.add_reaction("👍")
                await message.add_reaction("👎")
            except discord.errors.Forbidden:
                print(f"メッセージの公開または反応の追加に失敗しました: 権限不足 (Channel: {message.channel.id})")
            except Exception as e:
                print(f"メッセージの処理中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"on_messageイベントでエラーが発生しました: {e}")

bot.run(TOKEN)