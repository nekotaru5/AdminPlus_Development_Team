import json
import discord
from discord import app_commands
from datetime import datetime, timezone, timedelta
import pytz
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
tree = bot.tree

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


@bot.event
async def on_ready():
    global allowed_roles, announcement_channels
    allowed_roles = load_allowed_roles()
    announcement_channels = load_announcement_channels()

    # ステータスを「視聴中 nekotaru5」に設定
    activity = discord.Activity(type=discord.ActivityType.watching, name="nekotaru5のYouTubeChを視聴中")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    try:
        await bot.tree.sync()
        print("コマンドを同期しました")
    except Exception as e:
        print(f"コマンドの同期に失敗: {e}")

    print(f"{bot.user} としてログインしました")

@bot.command()
async def Admin(ctx):
    await ctx.send('( ˙꒳​˙ )))ｳﾝｳﾝ!!それで?それで?なんか用????')

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

@bot.tree.command(name="whitelist", description="許可ロールを表示します")
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
@bot.tree.command(name="add_announcement_list", description="自動アナウンス公開リストにチャンネルを追加します。")
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
        await interaction.response.send_message(f"{channel.mention} を自動アナウンス公開リストに追加しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} は既に自動アナウンス公開リストにあります。", ephemeral=True)

@bot.tree.command(name="announcement_list", description="自動アナウンス公開リストを表示します")
async def announcement_list(interaction: discord.Interaction):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in announcement_channels or not announcement_channels[guild_id]:
        await interaction.response.send_message("自動アナウンス公開リストにチャンネルはありません。", ephemeral=True)
        return

    channels = [f"<#{channel_id}>" for channel_id in announcement_channels[guild_id]]
    await interaction.response.send_message("アナウンスチャンネル:\n" + "\n".join(channels), ephemeral=True)

@bot.tree.command(name="delete_announcement_list", description="自動アナウンス公開リストからチャンネルを削除します。")
@app_commands.describe(channel="削除するチャンネル")
async def delete_announcement_list(interaction: discord.Interaction, channel: discord.TextChannel):
    if not await check_permissions(interaction):
        await interaction.response.send_message("このコマンドを実行する権限がありません", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    if guild_id in announcement_channels and channel.id in announcement_channels[guild_id]:
        announcement_channels[guild_id].remove(channel.id)
        save_announcement_channels()
        await interaction.response.send_message(f"{channel.mention} を自動アナウンス公開リストから削除しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} は自動アナウンス公開リストに含まれていません。", ephemeral=True)

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

@bot.tree.command(name="server_information", description="サーバー情報を表示します。")
async def server_information(interaction: discord.Interaction):
    guild = interaction.guild
    members = guild.members
    bots = [m for m in members if m.bot]
    users = [m for m in members if not m.bot]
    online = [m for m in members if m.status != discord.Status.offline]
    offline = [m for m in members if m.status == discord.Status.offline]

    categories = len(guild.categories)
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    total_channels = text_channels + voice_channels

    jst = pytz.timezone('Asia/Tokyo')
    created_at_jst = guild.created_at.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S')

    daily_message_count = 20
    max_messages = 200
    inactivity = max(0, min(100, 100 - int((daily_message_count / max_messages) * 100)))

    embed = discord.Embed(
        title=f"{guild.name} のサーバー情報",
        color=discord.Color.blue()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="メンバー数", value=f"ユーザー: {len(users)}\nBot: {len(bots)}", inline=True)
    embed.add_field(name="ステータス", value=f"オンライン: {len(online)}\nオフライン: {len(offline)}", inline=True)
    embed.add_field(name="サーバー創設日(JST)", value=created_at_jst, inline=False)
    embed.add_field(name="過疎度", value=f"{inactivity}%", inline=True)
    embed.add_field(name="カテゴリー数", value=str(categories), inline=True)
    embed.add_field(name="チャンネル数", value=str(total_channels), inline=True)

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
        message = f"{message}\n\nby {interaction.user.mention}"

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

@bot.tree.command(name="support", description="サポートサーバーの招待リンクを表示します")
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="サポートサーバー",
        description="サポートが必要な場合は、以下のリンクからサーバーに参加してください",
        color=discord.Color.blue()
    )
    embed.add_field(name="招待リンク", value="https://discord.gg/Yv9uJ32KkT")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="コマンドの詳細を表示します。")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="コマンド一覧",
        description="Botで使用できるコマンドの概要です。",
        color=discord.Color.green()
    )

    embed.add_field(
        name="■ 管理者専用",
        value=(
            "`/add_whitelist` - コマンド許可ロールを追加\n"
            "`/whitelist` - コマンド許可ロール一覧を表示\n"
            "`/delete_whitelist` - コマンド許可ロールを削除"
        ),
        inline=False
    )

    embed.add_field(
        name="■ 管理者 + 許可ロール",
        value=(
            "`/message` - 指定チャンネルにメッセージ送信（メンション・改行可）\n"
            "`/add_announcement_list` - 自動アナウンス公開リストにチャンネルを追加\n"
            "`/announcement_list` - 自動アナウンス公開リストを表示\n"
            "`/delete_announcement_list` - 自動アナウンス公開リストからチャンネルを削除"
        ),
        inline=False
    )

    embed.add_field(
        name="■ 全ユーザー利用可",
        value=(
            "`/server_information` - サーバー情報を表示\n"
            "`/user_information` - ユーザー情報を表示\n"
            "`/support` - サポートサーバーの招待リンクを表示\n"
            "`/help` - コマンドの詳細を表示"
        ),
        inline=False
    )

    embed.set_footer(text="ご不明点等がございましたら、サポートサーバーに問い合わせてください。")
    await interaction.response.send_message(embed=embed)  # ← ephemeral=False にする or 削除でOK

@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author.bot:
            return

        # メンションでヘルプ表示
        if bot.user in message.mentions:
            embed = discord.Embed(
                title="コマンド一覧",
                description="Botで使用できるコマンドの概要です。",
                color=discord.Color.green()
            )

            embed.add_field(
                name="■ 管理者専用",
                value=(
                    "`/add_whitelist` - コマンド許可ロールを追加\n"
                    "`/whitelist` - コマンド許可ロール一覧を表示\n"
                    "`/delete_whitelist` - コマンド許可ロールを削除"
                ),
                inline=False
            )

            embed.add_field(
                name="■ 管理者 + 許可ロール",
                value=(
                    "`/message` - 指定チャンネルにメッセージ送信（メンション・改行可）\n"
                    "`/add_announcement_list` - 自動アナウンス公開リストにチャンネルを追加\n"
                    "`/announcement_list` - 自動アナウンス公開リストを表示\n"
                    "`/delete_announcement_list` - 自動アナウンス公開リストからチャンネルを削除"
                ),
                inline=False
            )

            embed.add_field(
                name="■ 全ユーザー利用可",
                value=(
                    "`/server_information` - サーバー情報を表示\n"
                    "`/user_information` - ユーザー情報を表示\n"
                    "`/support` - サポートサーバーの招待リンクを表示\n"
                    "`/help` - コマンドの詳細を表示"
                ),
                inline=False
            )

            embed.add_field(
                name="サポートサーバー",
                value="[こちらをクリック](https://discord.gg/Yv9uJ32KkT)",
                inline=False
            )

            embed.set_footer(text="ご不明点等がございましたら、サポートサーバーまでお問い合わせください。")
            await message.channel.send(embed=embed)

        # アナウンス公開処理
        if message.guild:
            guild_id = str(message.guild.id)
            if guild_id in announcement_channels and message.channel.id in announcement_channels[guild_id]:
                try:
                    await message.publish()
                    await message.add_reaction("✅")
                    await message.add_reaction("👍")
                    await message.add_reaction("👎")
                except discord.errors.Forbidden:
                    print(f"権限不足でメッセージの公開またはリアクションの追加に失敗 (Channel: {message.channel.id})")
                except Exception as e:
                    print(f"メッセージの処理中にエラーが発生: {e}")

    except Exception as e:
        print(f"on_messageイベントでエラーが発生: {e}")

    await bot.process_commands(message)


bot.run(TOKEN)