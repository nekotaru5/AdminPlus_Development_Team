import json
import discord
from discord import app_commands
from datetime import datetime, timezone, timedelta
import pytz
from discord.ext import tasks
from discord.ext import commands
from discord import Object
import os
from threading import Thread
from flask import Flask
import requests
import time
import threading


app = Flask('')

@app.route('/')
def home():
    return """
    <html>
      <head><title>AdminPlus稼働状況</title></head>
      <body style="font-family: '游ゴシック', YuGothic, sans-serif; text-align: center; margin-top: 50px;">
        <h1>🚀 AdminPlusは現在稼働中です。</h1>
        <p>問題なく稼働しています。</p>
        <p>いつもご利用ありがとうございます</p>
      </body>
    </html>
    """
def run():
    app.run(host='0.0.0.0', port=8080)

def ping_loop(url):
    while True:
        try:
            response = requests.get(url)
            print(f'Pinged {url}: {response.status_code}')
        except Exception as e:
            print(f'Ping error: {e}')
        time.sleep(300)

# Flask起動用のスレッドを立てる
Thread(target=run).start()

# ここでping_loopを別スレッドで動かす
threading.Thread(target=ping_loop, args=('https://adminplus-development-team.onrender.com',), daemon=True).start()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("エラー: 環境変数 DISCORD_BOT_TOKEN が設定されていません。")
    exit(1)

# intentsを設定（全部有効化）
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
tree = bot.tree

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# グローバル変数で保持

admin_plus_list = []

def load_admin_plus():
    global admin_plus_list
    try:
        with open("AdminPlus.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("AdminPlus.jsonの形式がリストではありません。初期化します。")
                admin_plus_list = []
            else:
                admin_plus_list = data
    except Exception as e:
        print(f"[AdminPlus] ファイル読み込みエラー: {e}")
        admin_plus_list = []

def save_admin_plus():
    with open("AdminPlus.json", "w", encoding="utf-8") as f:
        json.dump(admin_plus_list, f, indent=4, ensure_ascii=False)

report_channels = {}

def load_report_channels():
    try:
        with open("report_channels.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[report_channels] 読み込みエラー: {e}")
        return {}

def save_report_channels():
    with open("report_channels.json", "w", encoding="utf-8") as f:
        json.dump(report_channels, f, indent=4)

update_channels = {}

def load_update_channels():
    try:
        with open("update_channel.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[update_channel.json] 読み込みエラー: {e}")
        return {}

def save_update_channels():
    with open("update_channel.json", "w", encoding="utf-8") as f:
        json.dump(update_channels, f, indent=4)

update_channels = {}

def load_update_channels():
    try:
        with open("update_channel.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[update_channel.json] 読み込みエラー: {e}")
        return {}

def save_update_channels():
    with open("update_channel.json", "w", encoding="utf-8") as f:
        json.dump(update_channels, f, indent=4)

white_list = []

def load_white_list():
    global white_list
    try:
        with open("Whitelist.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Whitelist.jsonの形式がリストではありません。初期化します。")
                white_list = []
            else:
                white_list = data
    except Exception as e:
        print(f"[Whitelist] ファイル読み込みエラー: {e}")
        white_list = []

def save_white_users():
    with open("Whitelist.json", "w", encoding="utf-8") as f:
        json.dump(white_list, f, indent=4, ensure_ascii=False)
# 許可ロールの管理
# 誕生日リスト（ユーザーID: "YYYY-MM-DD"）
log_channels = {}

def load_log_channels():
    try:
        with open("log_channels.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[log_channels] 読み込みエラー: {e}")
        return {}

def save_log_channels():
    with open("log_channels.json", "w") as f:
        json.dump(log_channels, f, indent=4)

birthday_list = {}

def load_birthday_list():
    try:
        with open("BirthdayList.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[BirthdayList] 読み込みエラー: {e}")
        return {}

def save_birthday_list():
    with open("BirthdayList.json", "w") as f:
        json.dump(birthday_list, f, indent=4)
# 誕生日アナウンスチャンネル（ギルドID: チャンネルID）
birthday_channels = {}

def load_birthday_channels():
    try:
        with open("Birthdaynotification.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Birthdaynotification] 読み込みエラー: {e}")
        return {}

def save_birthday_channels():
    with open("Birthdaynotification.json", "w") as f:
        json.dump(birthday_channels, f, indent=4)

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
async def can_modify_birthday(interaction: discord.Interaction, target_user_id: int) -> bool:
    member = await interaction.guild.fetch_member(interaction.user.id)

    if interaction.user.id == target_user_id:
        return True

    if member.guild_permissions.administrator:
        return True

    guild_id = str(interaction.guild_id)
    allowed = allowed_roles.get(guild_id, [])
    if any(role.id in allowed for role in member.roles):
        return True

    return False

# 🔧 ログを送る先のチャンネルID（数値）を指定
LOG_CHANNEL_ID = 1384839728393617539  # ← 実際のチャンネルIDに置き換え

async def send_log(bot, content, *, embed: discord.Embed = None):
    await bot.wait_until_ready()
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        try:
            if embed:
                await channel.send(content=content or None, embed=embed)
            else:
                await channel.send(content)
        except Exception as e:
            print(f"[ログ送信エラー] {e}")

async def do_update_status():
    guild_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"AdminPlusは{guild_count}個のサーバーに導入されています"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

@tasks.loop(minutes=1)
async def update_status_loop():
    await do_update_status()

@update_status_loop.before_loop
async def before_update_status():
    await bot.wait_until_ready()


@tasks.loop(minutes=1)
async def check_birthdays():
    now = datetime.now(timezone(timedelta(hours=9)))  # JST
    if now.hour == 12 and now.minute == 0:
        today = now.strftime("%m-%d")

        for guild_id, channel_id in birthday_channels.items():
            guild = bot.get_guild(int(guild_id))
            channel = bot.get_channel(channel_id)
            if not guild or not channel:
                continue

            birthday_messages = []
            for user_id, birth_date in birthday_list.items():
                if birth_date[5:] == today:
                    member = guild.get_member(int(user_id))
                    if member:
                        birthday_messages.append(f"🎉 {member.mention} さん、お誕生日おめでとうございます！ 🎉")
                        print(f"[{guild_id}] にて {user_id} の誕生日を祝いました")
                        await send_log(f"[{guild_id}] にて {user_id} の誕生日を祝いました")

            if birthday_messages:
                await channel.send("\n".join(birthday_messages))

@check_birthdays.before_loop
async def before_birthday_check():
    await bot.wait_until_ready()
# ←ここで呼ばずに、

@bot.event
async def on_ready():
    global allowed_roles, announcement_channels, birthday_list, birthday_channels
    global log_channels,white_list, update_channels, admin_plus_list

    allowed_roles = load_allowed_roles()
    announcement_channels = load_announcement_channels()
    birthday_list = load_birthday_list()
    birthday_channels = load_birthday_channels()
    log_channels = load_log_channels()
    white_list = load_white_list()  # ←ここ修正！
    update_channels = load_update_channels()
    admin_plus_list = load_admin_plus_list()

    if not check_birthdays.is_running():
        check_birthdays.start()

    if not update_status_loop.is_running():
        update_status_loop.start()

    await do_update_status()

    try:
        await bot.tree.sync()
        await send_log(bot, "コマンドを同期しました")
    except Exception as e:
        print(f"コマンドの同期に失敗: {e}")
        await send_log(bot, f"コマンドの同期に失敗: {e}")

    print(f"{bot.user} としてログインしました")
    await send_log(bot, f"{bot.user} としてログインしました")

# 非公開用（ephemeral）ヘルプ
class ServerListView(discord.ui.View):
    def __init__(self, guilds, user: discord.User, timeout=60):
        super().__init__(timeout=timeout)
        self.guilds = guilds
        self.user = user
        self.page = 0
        self.per_page = 10

    def get_page_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        chunk = self.guilds[start:end]

        embed = discord.Embed(
            title=f"Botが参加しているサーバー一覧 ({len(self.guilds)}個中 {start+1}〜{min(end, len(self.guilds))})",
            color=discord.Color.green()
        )

        for g in chunk:
            icon_url = g.icon.url if g.icon else "https://cdn.discordapp.com/embed/avatars/0.png"
            name = f"**{g.name}**"
            value = f"[🖼️サーバーアイコン]({icon_url})\n👥 メンバー数: {g.member_count}\n🚀 ブースト数:{g.premium_subscription_count}回 / レベル:{g.premium_tier}レベル"
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=f"ページ {self.page + 1} / {((len(self.guilds) - 1) // self.per_page) + 1}")
        return embed

    def update_buttons(self):
        # ボタンが存在する前に呼ばれないようにする
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.label == "◀ 戻る":
                    item.disabled = self.page == 0
                elif item.label == "次へ ▶":
                    item.disabled = (self.page + 1) * self.per_page >= len(self.guilds)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user.id

    @discord.ui.button(label="◀ 戻る", style=discord.ButtonStyle.secondary, disabled=True)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="次へ ▶", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

def build_help_embed_and_view_ephemeral():
    import discord

    # 最初のヘルプEmbed（コマンド一覧）
    def main_help_embed():
        embed = discord.Embed(
            title="コマンド一覧",
            description="カテゴリを選んで、使用可能なコマンドを確認してください。",
            color=0x3498db
        )
        embed.add_field(
            name="🔗 サポートサーバー",
            value="[こちらを押してください](https://discord.gg/ku8gdut5U2) でサポートサーバーに参加できます。",
            inline=False
        )
        embed.set_footer(text="不明点があればサポートサーバーをご利用ください。")
        return embed

    class HelpSelect(discord.ui.Select):
        def __init__(self, parent_view: discord.ui.View):
            options = [
                discord.SelectOption(label="■ ヘルプに戻る", value="help", description="最初のコマンド一覧に戻る"),
                discord.SelectOption(label="■ 管理者専用", value="admin", description="管理者専用のコマンド一覧"),
                discord.SelectOption(label="■ 管理者 + 許可ロール", value="authorized", description="許可された人のコマンド一覧"),
                discord.SelectOption(label="■ 全ユーザー利用可", value="everyone", description="誰でも使えるコマンド一覧")
            ]
            super().__init__(
                placeholder="カテゴリを選んでください",
                min_values=1,
                max_values=1,
                options=options
            )
            self.parent_view = parent_view

        async def callback(self, interaction: discord.Interaction):
            category = self.values[0]

            if category == "help":
                embed = main_help_embed()
            elif category == "admin":
                embed = discord.Embed(title="■ 管理者専用コマンド", color=0xff5555)
                embed.add_field(name="/add_whitelist", value="コマンド許可ロールを追加", inline=False)
                embed.add_field(name="/whitelist", value="コマンド許可ロール一覧を表示", inline=False)
                embed.add_field(name="/delete_whitelist", value="コマンド許可ロールを削除", inline=False)
            elif category == "authorized":
                embed = discord.Embed(title="■ 管理者 + 許可ロール", color=0xffaa00)
                embed.add_field(name="/message", value="指定チャンネルにメッセージ送信（メンション・改行可）", inline=False)
                embed.add_field(name="/add_announcement_list", value="自動アナウンス公開リストにチャンネルを追加", inline=False)
                embed.add_field(name="/announcement_list", value="自動アナウンス公開リストを表示", inline=False)
                embed.add_field(name="/delete_announcement_list", value="自動アナウンス公開リストからチャンネルを削除", inline=False)
                embed.add_field(name="/birthdaych_list", value="誕生日通知チャンネルを表示", inline=False)
                embed.add_field(name="/setbirthdaych", value="誕生日通知チャンネルを登録・解除", inline=False)
                embed.add_field(name="/birthday_list", value="登録されている誕生日を表示", inline=False)
                embed.add_field(name="/add_birthdaylist", value="誕生日を登録", inline=False)
            elif category == "everyone":
                embed = discord.Embed(title="■ 全ユーザー利用可", color=0x55ff55)
                embed.add_field(name="/server_information", value="サーバー情報を表示", inline=False)
                embed.add_field(name="/user_information", value="ユーザー情報を表示", inline=False)
                embed.add_field(name="/support", value="サポートサーバーのURLを表示", inline=False)
                embed.add_field(name="/help または !help", value="コマンドの詳細を表示", inline=False)
                embed.add_field(name="/add_birthdaylist", value="誕生日を登録", inline=False)
                embed.add_field(name="/birthday_list", value="登録されている誕生日を表示", inline=False)

            await interaction.response.edit_message(embed=embed, view=self.parent_view)

    class HelpView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.select = HelpSelect(self)
            self.add_item(self.select)

    view = HelpView()
    return main_help_embed(), view

# ──────────────
# 公開用ヘルプ（編集可能メッセージを使う）
b_message_public = None  # グローバル変数でメッセージ保持

def build_help_embed_and_view_public():
    embed = discord.Embed(
        title="コマンド一覧",
        description="カテゴリを選んで、使用可能なコマンドを確認してください。",
        color=0x3498db
    )
    embed.add_field(
        name="🔗 サポートサーバー",
        value="[こちらを押してください](https://discord.gg/ku8gdut5U2) でサポートサーバーに参加できます。",
        inline=False
    )
    embed.set_footer(text="不明点があればサポートサーバーをご利用ください。")

    class HelpSelect(discord.ui.Select):
        def __init__(self, parent_view: discord.ui.View):
            options = [
                discord.SelectOption(label="■ 管理者専用", value="admin", description="管理者専用のコマンド一覧"),
                discord.SelectOption(label="■ 管理者 + 許可ロール", value="authorized", description="許可された人のコマンド一覧"),
                discord.SelectOption(label="■ 全ユーザー利用可", value="everyone", description="誰でも使えるコマンド一覧")
            ]
            super().__init__(
                placeholder="カテゴリを選んでください",
                min_values=1,
                max_values=1,
                options=options
            )
            self.parent_view = parent_view

        async def callback(self, interaction: discord.Interaction):
            global b_message_public
            category = self.values[0]

            if category == "admin":
                detail_embed = discord.Embed(title="■ 管理者専用コマンド", color=0xff5555)
                detail_embed.add_field(name="/add_whitelist", value="コマンド許可ロールを追加", inline=False)
                detail_embed.add_field(name="/whitelist", value="コマンド許可ロール一覧を表示", inline=False)
                detail_embed.add_field(name="/delete_whitelist", value="コマンド許可ロールを削除", inline=False)

            elif category == "authorized":
                detail_embed = discord.Embed(title="■ 管理者 + 許可ロール", color=0xffaa00)
                detail_embed.add_field(name="/message", value="指定チャンネルにメッセージ送信（メンション・改行可）", inline=False)
                detail_embed.add_field(name="/add_announcement_list", value="自動アナウンス公開リストにチャンネルを追加", inline=False)
                detail_embed.add_field(name="/announcement_list", value="自動アナウンス公開リストを表示", inline=False)
                detail_embed.add_field(name="/delete_announcement_list", value="自動アナウンス公開リストからチャンネルを削除", inline=False)
                detail_embed.add_field(name="/birthdaych_list", value="誕生日通知チャンネルを表示", inline=False)
                detail_embed.add_field(name="/setbirthdaych", value="誕生日通知チャンネルを登録・解除", inline=False)
                detail_embed.add_field(name="/birthday_list", value="登録されている誕生日を表示", inline=False)
                detail_embed.add_field(name="/add_birthdaylist", value="誕生日を登録", inline=False)

            elif category == "everyone":
                detail_embed = discord.Embed(title="■ 全ユーザー利用可", color=0x55ff55)
                detail_embed.add_field(name="/server_information", value="サーバー情報を表示", inline=False)
                detail_embed.add_field(name="/user_information", value="ユーザー情報を表示", inline=False)
                detail_embed.add_field(name="/support", value="サポートサーバーのURLを表示", inline=False)
                detail_embed.add_field(name="/help または !help", value="コマンドの詳細を表示", inline=False)
                detail_embed.add_field(name="/add_birthdaylist", value="誕生日を登録", inline=False)
                detail_embed.add_field(name="/birthday_list", value="登録されている誕生日を表示", inline=False)

            await interaction.response.defer()

            if b_message_public is None:
                b_message_public = await interaction.channel.send(embed=detail_embed)
            else:
                await b_message_public.edit(embed=detail_embed)

    class HelpView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(HelpSelect(self))

    view = HelpView()
    return embed, view


# バージョン情報リスト
updates = [
    {
        "version": "1.3",
        "add": [
            "DM機能を追加しました（Adminplus管理者のみ利用可能です）"
        ],
        "change": [
            "Update、!Update、/help、!helpコマンドの表示方法と表示場所を変更。",
            "「!」コマンドはDMで、「/」コマンドはプライベートメッセージで表示されます。",
            "ボタンが追加され、埋め込みが見やすくなりました。"
        ],
        "fix": []
    },
    {
        "version": "1.2",
        "add": [
            "/helpと!helpを追加。プレフィックスコマンドとスラッシュコマンドで実行可能（誰でもOK）",
            "/logchコマンドを追加。メッセージログを受信（管理者or許可ロールが必要）"
        ],
        "change": [],
        "fix": []
    },
    {
        "version": "1.1",
        "add": [
            "アップデート履歴表示機能を追加。/update と !update で実行可能（誰でもOK）"
        ],
        "change": [],
        "fix": []
    },
    {
        "version": "1.0",
        "add": [
            "/setbirthdaych [チャンネル]：誕生日通知用チャンネルの登録・解除（管理者or許可ロールが必要）",
            "/birthdaych_list：登録済みの誕生日通知チャンネルを一覧表示（管理者or許可ロールが必要）",
            "/add_birthdaylist [ユーザー] [YYYY-MM-DD]：誕生日登録（自分は誰でもOK、他人は管理者or許可ロールが必要）",
            "/delete_birthdaylist [ユーザー]：誕生日削除（自分は誰でもOK、他人は管理者or許可ロールが必要）",
            "/birthday_list：全ユーザーの誕生日を確認（管理者or許可ロールが必要）"
        ],
        "change": [],
        "fix": []
    }
]

def format_update_content(update):
    content = ""
    if update["add"]:
        content += "**追加点**\n" + "\n".join(f"{i+1}. {line}" for i, line in enumerate(update["add"])) + "\n\n"
    if update["change"]:
        content += "**変更点**\n" + "\n".join(f"{i+1}. {line}" for i, line in enumerate(update["change"])) + "\n\n"
    if update["fix"]:
        content += "**修正点**\n" + "\n".join(f"{i+1}. {line}" for i, line in enumerate(update["fix"])) + "\n"
    return content.strip()


def build_update_embed_and_view_ephemeral():
    import discord

    latest = updates[0]
    embed = discord.Embed(
        title=f"🛠️ アップデート履歴 Version {latest['version']}",
        description=format_update_content(latest),
        color=discord.Color.orange()
    )
    embed.set_footer(text="最終更新: 2025年6月4日")
    embed.set_author(name="Admin Plus Development Team")

    class UpdateSelect(discord.ui.Select):
        def __init__(self, parent_view: discord.ui.View):
            self.parent_view = parent_view
            options = [
                discord.SelectOption(label=f"Version {u['version']}", value=str(i))
                for i, u in enumerate(updates)
            ]
            super().__init__(
                placeholder="バージョンを選択してください",
                min_values=1,
                max_values=1,
                options=options
            )

        async def callback(self, interaction: discord.Interaction):
            index = int(self.values[0])
            selected = updates[index]
            new_embed = discord.Embed(
                title=f"🛠️ アップデート履歴 Version {selected['version']}",
                description=format_update_content(selected),
                color=discord.Color.orange()
            )
            new_embed.set_footer(text="最終更新: 2025年6月4日")
            new_embed.set_author(name="Admin Plus Development Team")
            await interaction.response.edit_message(embed=new_embed)

    class UpdateView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(UpdateSelect(self))

    view = UpdateView()
    return embed, view


def build_update_embed_and_view_public():
    import discord

    latest = updates[0]
    embed = discord.Embed(
        title=f"🛠️ アップデート履歴 Version {latest['version']}",
        description=format_update_content(latest),
        color=discord.Color.orange()
    )
    embed.set_footer(text="最終更新: 2025年6月4日")
    embed.set_author(name="Admin Plus Development Team")

    class UpdateSelect(discord.ui.Select):
        def __init__(self, parent_view: discord.ui.View):
            self.parent_view = parent_view
            options = [
                discord.SelectOption(label=f"Version {u['version']}", value=str(i))
                for i, u in enumerate(updates)
            ]
            super().__init__(
                placeholder="バージョンを選択してください",
                min_values=1,
                max_values=1,
                options=options
            )

        async def callback(self, interaction: discord.Interaction):
            index = int(self.values[0])
            selected = updates[index]
            new_embed = discord.Embed(
                title=f"🛠️ アップデート履歴 Version {selected['version']}",
                description=format_update_content(selected),
                color=discord.Color.orange()
            )
            new_embed.set_footer(text="最終更新: 2025年6月22日")
            new_embed.set_author(name="AdminPlus Development Team")
            await interaction.response.edit_message(embed=new_embed)

    class UpdateView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(UpdateSelect(self))

    view = UpdateView()
    return embed, view

class WhiteUserRequestModal(discord.ui.Modal, title="ホワイトリスト申請フォーム"):
    admin_server = discord.ui.TextInput(
        label="管理しているサーバー名と招待リンク（必須）",
        placeholder="例: Admin Plus Support https://discord.gg/Yv9uJ32KkT",
        required=True,
    )
    mod_server = discord.ui.TextInput(
        label="モデレーターをしているサーバー名と招待リンク（任意）",
        placeholder="例: 猫山高速鉄道 https://discord.gg/TVf2R29t6k",
        required=False,
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        user = self.interaction.user
        guild = self.interaction.guild

        embed = discord.Embed(
            title="📨 ホワイトリスト申請",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="🧑‍💻 コマンドを実行したユーザー",
            value=f"{user.mention} (`{user}`)\nID: `{user.id}`",
            inline=False
        )
        embed.add_field(
            name="🌐 実行されたサーバー",
            value=f"{guild.name} (`{guild.id}`)",
            inline=False
        )
        embed.add_field(
            name="🛠️ 管理しているサーバー",
            value=self.admin_server.value,
            inline=False
        )
        embed.add_field(
            name="👮 モデレーターをしているサーバー",
            value=self.mod_server.value or "（なし）",
            inline=False
        )
        embed.set_footer(text="※サポートサーバーに参加していない場合は無効です")

        await interaction.response.send_message("✅ 申請を送信しました！", ephemeral=True)
        await send_log(bot, None, embed=embed)

# ✅ !update（従来のプレフィックスコマンド）
@bot.command(name="update")
async def update(ctx):
    embed, view = build_update_embed_and_view_public()
    try:
        await ctx.author.send(embed=embed, view=view)
        # 送信完了の通知はなしにするならコメントアウト
        # await ctx.send("アップデート情報をDMで送りました！")
    except discord.Forbidden:
        await ctx.send("DMを送れませんでした。DM受信を許可してください。")

@bot.command(name="help")
async def help(ctx):
    embed, view = build_help_embed_and_view_public()  # 公開用の関数を呼ぶ
    try:
        dm_channel = await ctx.author.create_dm()
        await dm_channel.send(embed=embed, view=view)
    except discord.Forbidden:
        # DM拒否されてたら無視（通知もしない）
        pass


# ✅ /update（新しいスラッシュコマンド）
@bot.tree.command(name="request", description="ホワイトリスト申請フォーム")
@app_commands.checks.has_permissions(administrator=True)
async def request(interaction: discord.Interaction):
    await interaction.response.send_modal(WhiteUserRequestModal(interaction))

@bot.tree.command(name="update_message", description="すべてのアップデートチャンネルに一斉送信（ホワイトユーザーのみ）")
@app_commands.describe(message="送信する内容（改行・メンション可）")
async def update_message(interaction: discord.Interaction, message: str):
    # ホワイトユーザー制限
    if str(interaction.user.id) not in map(str, admin_plus_list):
        await interaction.response.send_message(
            "❌ あなたにはこのコマンドを実行する権限がありません（Admin plus 管理者専用）。",
            ephemeral=True
        )
        return

    # メッセージ送信処理
    count = 0
    for guild_id, channel_id in update_channels.items():
        guild = bot.get_guild(int(guild_id))
        if not guild:
            continue
        channel = guild.get_channel(channel_id)
        if not channel:
            continue
        try:
            await channel.send(message)
            count += 1
        except Exception as e:
            print(f"[エラー] {guild_id} の送信に失敗: {e}")

    await interaction.response.send_message(
        f"✅ {count} チャンネルにメッセージを送信しました。",
        ephemeral=True
    )

    # ログ出力
    print(f"✅ {interaction.user} が /update_message を実行し、{count} チャンネルに送信しました。")
    await send_log(f"✅ {interaction.user} が /update_message を実行し、{count} チャンネルに送信しました。")

@bot.tree.command(name="updatech", description="アップデートチャンネルを設定（管理者または許可ロールのみ）")
@app_commands.describe(channel="送信先チャンネル")
async def updatech(interaction: discord.Interaction, channel: discord.TextChannel):
    global update_channels

    if not await check_permissions(interaction):
        await interaction.response.send_message(
            "❌ このコマンドを実行する権限がありません（管理者または許可ロール限定）。",
            ephemeral=True
        )
        return

    guild_id = str(interaction.guild_id)
    update_channels[guild_id] = channel.id
    save_update_channels()

    # ユーザーへの返信
    await interaction.response.send_message(
        f"✅ アップデートチャンネルを {channel.mention} に設定しました。",
        ephemeral=True
    )

    # ✅ コンソールログ出力
    print(f"[{guild_id}] で、[{channel.id}] にアップデートチャンネルが設定されました。")
    await send_log(f"[{guild_id}] で、[{channel.id}] にアップデートチャンネルが設定されました。")
@bot.tree.command(name="server_list", description="Botが参加しているサーバー一覧を表示（ページ付き）")
async def server_list(interaction: discord.Interaction):
    guilds = bot.guilds
    view = ServerListView(guilds, interaction.user)

    await interaction.response.send_message(
        embed=view.get_page_embed(),
        view=view,
        ephemeral=True
    )

@bot.tree.context_menu(name="メッセージを通報する")
async def report_message(interaction: discord.Interaction, message: discord.Message):
    guild_id = str(interaction.guild_id)
    report_channel_id = report_channels.get(guild_id)

    if not report_channel_id:
        await interaction.response.send_message("⚠️ 通報チャンネルが設定されていません。", ephemeral=True)
        return

    report_channel = interaction.client.get_channel(report_channel_id)
    if not report_channel:
        await interaction.response.send_message("⚠️ 通報チャンネルが見つかりません。", ephemeral=True)
        return

    message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

    embed = discord.Embed(
        title="通報されました",
        color=discord.Color.red()
    )
    embed.add_field(name="通報者", value=f"`{interaction.user.name}`", inline=False)
    embed.add_field(name="対象メッセージ", value=f"[こちら]({message_link})", inline=False)
    embed.timestamp = discord.utils.utcnow()

    await report_channel.send(embed=embed)
    await interaction.response.send_message("✅ 通報を送信しました。", ephemeral=True)

@bot.tree.command(name="reportch", description="通報チャンネルを設定します（管理者または許可ロール限定）")
async def set_report_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not await check_permissions(interaction):
        await interaction.response.send_message("❌ このコマンドを実行する権限がありません。", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    report_channels[guild_id] = channel.id
    save_report_channels()

    # ログ出力
    print(f"[通報設定] サーバーID: {guild_id} にチャンネルID: {channel.id} を通報用チャンネルとして設定しました")
    await send_log(bot, f"[通報設定] サーバーID: {guild_id} にチャンネルID: {channel.id} を通報用チャンネルとして設定しました")

    await interaction.response.send_message(f"✅ 通報チャンネルを {channel.mention} に設定しました。", ephemeral=True)

@bot.tree.command(name="dm", description="指定したユーザーにDMを送信します。")
@app_commands.describe(user="DMを送る相手", message="送信するメッセージ")
async def dm(interaction: discord.Interaction, user: discord.User, message: str):
    if not white_list:
        await interaction.response.send_message("⚠️ 管理者リストがロードされていません。", ephemeral=True)
        return

    if interaction.user.id not in admin_plus_list:
        await interaction.response.send_message("❌ あなたにはこのコマンドを使う権限がありません。", ephemeral=True)
        return

    try:
        await user.send(message)
        await interaction.response.send_message(f"✅ {user.name} にDMを送りました。", ephemeral=True)
        print(f"[DM送信ログ] {interaction.user} が {user} に以下のDMを送信しました:\n{message}\n")
    except discord.Forbidden:
        await interaction.response.send_message("⚠️ 相手のDM設定により送信できません。", ephemeral=True)
        print(f"[送信失敗] {interaction.user} → {user}：DMが拒否された可能性あり")
    except Exception as e:
        await interaction.response.send_message(f"❌ エラーが発生しました: {e}", ephemeral=True)
        print(f"[エラー] {interaction.user} → {user}：{e}")

@bot.tree.command(name="delete_bot_message", description="Botが送信したメッセージを削除します（メッセージID指定）")
@app_commands.describe(message_id="削除したいメッセージのID")
async def delete_bot_message(interaction: discord.Interaction, message_id: str):
    if not await check_permissions(interaction):
        await interaction.response.send_message("❌ このコマンドを実行する権限がありません。", ephemeral=True)
        return

    try:
        channel = interaction.channel
        message = await channel.fetch_message(int(message_id))

        if message.author.id != bot.user.id:
            await interaction.response.send_message("⚠️ そのメッセージはBotが送信したものではありません。", ephemeral=True)
            return

        await message.delete()
        await interaction.response.send_message("✅ メッセージを削除しました。", ephemeral=True)

    except discord.NotFound:
        await interaction.response.send_message("⚠️ メッセージが見つかりませんでした。", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ メッセージの削除権限がありません。", ephemeral=True)
    except Exception as e:
        print(f"メッセージ削除エラー: {e}")
        await interaction.response.send_message("❌ メッセージの削除中にエラーが発生しました。", ephemeral=True)

@tree.command(name="logch", description="ログ送信先チャンネルを設定します（管理者または許可ロール限定）")
@app_commands.describe(channel="ログを送信するチャンネル")
async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not await check_permissions(interaction):
        await interaction.response.send_message("❌ このコマンドを実行する権限がありません。", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    is_new = guild_id not in log_channels  # 新規登録かどうか判定
    log_channels[guild_id] = channel.id
    save_log_channels()

    if is_new:
        print(f"✅ [{guild_id}] で、[{channel.id}] がログチャンネルとして登録されました。")
        await send_log(bot, f"✅ [{guild_id}] で、[{channel.id}] がログチャンネルとして登録されました。")
        await interaction.response.send_message(f"✅ ログチャンネルに登録しました： {channel.mention}", ephemeral=True)
    else:
        print(f"⚠️ [{guild_id}] で、[{channel.id}] にログチャンネルが上書きされました。")
        await send_log(bot, f"⚠️ [{guild_id}] で、[{channel.id}] にログチャンネルが上書きされました。")
        await interaction.response.send_message(f"⚠️ ログチャンネルを上書きしました： {channel.mention}", ephemeral=True)

@bot.tree.command(name="update", description="アップデート履歴を表示します")
async def slash_update(interaction: discord.Interaction):
    embed, view = build_update_embed_and_view_ephemeral()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.command()
async def Admin(ctx):
    await ctx.send('呼びましたか？(⁎˃ᴗ˂⁎)')

#　誕生日管理コマンド
@bot.tree.command(name="setbirthdaych", description="誕生日アナウンス用チャンネルを登録または解除します")
@app_commands.describe(channel="誕生日アナウンスを行うチャンネル")
async def set_birthday_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        member = await interaction.guild.fetch_member(interaction.user.id)
        if not member.guild_permissions.administrator:
            guild_id = str(interaction.guild_id)
            allowed = allowed_roles.get(guild_id, [])
            if not any(role.id in allowed for role in member.roles):
                await interaction.response.send_message("このコマンドは管理者または許可ロールのみ使用できます。", ephemeral=True)
                return
    except Exception as e:
        print(f"[setbirthdaych] 権限チェックエラー: {e}")
        await send_log(f"[setbirthdaych] 権限チェックエラー: {e}")
        await interaction.response.send_message("権限の確認中にエラーが発生しました。", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    existing_channel_id = birthday_channels.get(guild_id)

    if existing_channel_id == channel.id:
        del birthday_channels[guild_id]
        save_birthday_channels()
        await interaction.response.send_message(f"{channel.mention} を誕生日アナウンスチャンネルから解除しました。", ephemeral=True)
        print(f"[{guild_id}] で [{channel.id}] が誕生日アナウンスチャンネルから削除されました。")
        await send_log(f"[{guild_id}] で [{channel.id}] が誕生日アナウンスチャンネルから削除されました。")
        
    else:
        if existing_channel_id is not None:
            print(f"[{guild_id}] で誕生日アナウンスチャンネルを [{existing_channel_id}] から [{channel.id}] に上書きしました。")
            await send_log(f"[{guild_id}] で誕生日アナウンスチャンネルを [{existing_channel_id}] から [{channel.id}] に上書きしました。")
        else:
            print(f"[{guild_id}] で [{channel.id}] が誕生日アナウンスチャンネルとして登録されました。")
            await send_log(f"[{guild_id}] で [{channel.id}] が誕生日アナウンスチャンネルとして登録されました。")

        birthday_channels[guild_id] = channel.id
        save_birthday_channels()
        await interaction.response.send_message(f"{channel.mention} を誕生日アナウンスチャンネルに登録しました。", ephemeral=True)

@bot.tree.command(name="add_birthdaylist", description="誕生日を登録します")
@app_commands.describe(user="登録するユーザー", birthday="誕生日 (YYYY-MM-DD)")
async def add_birthdaylist(interaction: discord.Interaction, user: discord.User, birthday: str):
    if not await can_modify_birthday(interaction, user.id):
        await interaction.response.send_message("このユーザーの誕生日を登録する権限がありません。", ephemeral=True)
        return

    try:
        datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        await interaction.response.send_message("誕生日の形式が正しくありません。YYYY-MM-DD で入力してください。", ephemeral=True)
        return

    birthday_list[str(user.id)] = birthday
    save_birthday_list()
    await interaction.response.send_message(f"{user.mention} の誕生日を {birthday} に登録しました。", ephemeral=True)
    print(f"[{interaction.guild_id}] でユーザーID {user.id} の誕生日を {birthday} に登録しました。")
    await send_log(f"[{interaction.guild_id}] でユーザーID {user.id} の誕生日を {birthday} に登録しました。")

@bot.tree.command(name="delete_birthdaylist", description="誕生日を削除します")
@app_commands.describe(user="削除するユーザー")
async def delete_birthdaylist(interaction: discord.Interaction, user: discord.User):
    if not await can_modify_birthday(interaction, user.id):
        await interaction.response.send_message("このユーザーの誕生日を削除する権限がありません。", ephemeral=True)
        return

    if str(user.id) in birthday_list:
        del birthday_list[str(user.id)]
        save_birthday_list()
        await interaction.response.send_message(f"{user.mention} の誕生日を削除しました。", ephemeral=True)
        print(f"[{interaction.guild_id}] でユーザーID {user.id} の誕生日を削除しました。")
        await send_log(f"[{interaction.guild_id}] でユーザーID {user.id} の誕生日を削除しました。")
    else:
        await interaction.response.send_message(f"{user.mention} は誕生日リストに登録されていません。", ephemeral=True)

@bot.tree.command(name="birthday_list", description="登録されている誕生日リストを表示します")
async def show_birthday_list(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
        return

    # 管理者か、allowed_roles.json で許可されたロールを持っているかを確認
    if not interaction.user.guild_permissions.administrator:
        allowed_role_id = allowed_roles.get(str(guild.id))
        if not allowed_role_id or all(role.id != int(allowed_role_id) for role in interaction.user.roles):
            await interaction.response.send_message("このコマンドを使用する権限がありません。", ephemeral=True)
            return

    if not birthday_list:
        await interaction.response.send_message("誕生日リストは空です。", ephemeral=True)
        return

    message = "**🎂 登録済みの誕生日一覧 🎂**\n"
    count = 0
    for user_id, birthday in birthday_list.items():
        member = guild.get_member(int(user_id))
        if member:
            message += f"{member.mention} - {birthday}\n"
            count += 1

    if count == 0:
        await interaction.response.send_message("このサーバーには登録されている誕生日がありません。", ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)
@bot.tree.command(name="birthdaych_list", description="このサーバーの誕生日通知チャンネルを表示します（管理者または許可ロール限定）")
async def birthdaych_list(interaction: discord.Interaction):
    try:
        member = await interaction.guild.fetch_member(interaction.user.id)
        if not member.guild_permissions.administrator:
            guild_id = str(interaction.guild_id)
            allowed = allowed_roles.get(guild_id, [])
            if not any(role.id in allowed for role in member.roles):
                await interaction.response.send_message("このコマンドは管理者または許可ロールのみ使用できます。", ephemeral=True)
                return
    except Exception as e:
        print(f"[birthdaych_list] 権限チェックエラー: {e}")
        await send_log(f"[birthdaych_list] 権限チェックエラー: {e}")
        await interaction.response.send_message("権限の確認中にエラーが発生しました。", ephemeral=True)
        return

    guild_id = str(interaction.guild_id)
    channel_id = birthday_channels.get(guild_id)

    if not channel_id:
        await interaction.response.send_message("このサーバーには誕生日通知チャンネルが設定されていません。", ephemeral=True)
        return

    channel = interaction.guild.get_channel(channel_id) or bot.get_channel(channel_id)

    if channel:
        message = f"🎂 このサーバーの誕生日通知チャンネルは {channel.mention} です。"
    else:
        message = f"⚠️ 登録されたチャンネルID `{channel_id}` が見つかりません。削除された可能性があります。"

    await interaction.response.send_message(message, ephemeral=True)

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
        await send_log(f"権限チェックエラー: {e}")
        return

    guild_id = str(interaction.guild_id)
    if guild_id not in allowed_roles:
        allowed_roles[guild_id] = []

    if role.id not in allowed_roles[guild_id]:
        allowed_roles[guild_id].append(role.id)
        save_allowed_roles()
        print(f"[{guild_id}] でロール {role.id} が追加されました")
        await send_log(f"[{guild_id}] でロール {role.id} が追加されました") # ← ここ追加
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
        await send_log(f"権限チェックエラー: {e}")
        return

    guild_id = str(interaction.guild_id)
    if guild_id in allowed_roles and role.id in allowed_roles[guild_id]:
        allowed_roles[guild_id].remove(role.id)
        save_allowed_roles()
        print(f"[{guild_id}] でロール {role.id} が削除されました")
        await send_log(f"[{guild_id}] でロール {role.id} が削除されました")  # ← ここ追加
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
        await send_log(f"権限チェックエラー: {e}")
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
        print(f"[{guild_id}] でチャンネルID {channel.id} がアナウンスリストに追加されました")  # ← 追加
        await interaction.response.send_message(f"{channel.mention} を自動アナウンス公開リストに追加しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} は既に自動アナウンス公開リストにあります。", ephemeral=True)


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
        print(f"[{guild_id}] でチャンネルID {channel.id} がアナウンスリストから削除されました")
        await send_log(f"[{guild_id}] でチャンネルID {channel.id} がアナウンスリストから削除されました") # ← 追加
        await interaction.response.send_message(f"{channel.mention} を自動アナウンス公開リストから削除しました", ephemeral=True)
    else:
        await interaction.response.send_message(f"{channel.mention} は自動アナウンス公開リストに含まれていません。", ephemeral=True)

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

    boost_count = guild.premium_subscription_count
    boost_level = guild.premium_tier

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
    embed.add_field(name="ブースト数", value=f"{boost_count}回", inline=True)
    embed.add_field(name="ブーストレベル", value=f"レベル {boost_level}", inline=True)

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

@bot.tree.command(name="help", description="コマンド一覧を表示します")
async def help(interaction: discord.Interaction):
    embed, view = build_help_embed_and_view_ephemeral()  # 非公開用の関数名に合わせてください
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@request.error
async def request_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❌ このコマンドは管理者のみ使用可能です。", ephemeral=True
        )

@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author.bot:
            return

        # メンションでヘルプ表示（DM送信）
        if bot.user in message.mentions:
            embed, view = build_help_embed_and_view_public()
            try:
                await message.author.send(embed=embed, view=view)
            except discord.Forbidden:
                pass  # DM送信失敗は無視

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
                    await send_log(f"権限不足でメッセージの公開またはリアクションの追加に失敗 (Channel: {message.channel.id})")
                except Exception as e:
                    print(f"メッセージの処理中にエラーが発生: {e}")
                    await send_log(f"メッセージの処理中にエラーが発生: {e}")

    except Exception as e:
        print(f"on_messageイベントでエラーが発生: {e}")
        await send_log(f"on_messageイベントでエラーが発生: {e}")

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content:
        return

    ch_id = log_channels.get(str(before.guild.id))
    if not ch_id:
        return

    channel = bot.get_channel(ch_id)
    if not channel:
        return

    embed = discord.Embed(
        title="✏️ メッセージ編集",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="変更前", value=before.content or "（空）", inline=False)
    embed.add_field(name="変更後", value=after.content or "（空）", inline=False)
    embed.add_field(name="チャンネル", value=before.channel.mention)
    embed.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)

    await channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    ch_id = log_channels.get(str(message.guild.id))
    if not ch_id:
        return

    channel = bot.get_channel(ch_id)
    if not channel:
        return

    embed = discord.Embed(
        title="🗑️ メッセージ削除",
        description=message.content or "（空）",
        color=discord.Color.dark_grey(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="チャンネル", value=message.channel.mention)
    embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)

    await channel.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    await update_status()

@bot.event
async def on_guild_remove(guild):
    await update_status()
    
bot.run(TOKEN)
