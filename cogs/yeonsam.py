import discord
from discord.ext import commands
from utils.storage import get_guild, update_guild


# 🔹 Modal (현재 값 반영 + 미리보기 출력)
class EditModal(discord.ui.Modal):
    def __init__(self, guild_id):
        super().__init__(title="메시지 수정")
        self.guild_id = guild_id

        config = get_guild(guild_id)

        self.message = discord.ui.TextInput(
            label="출력 메시지",
            default=config["welcome_message"]
        )

        self.link = discord.ui.TextInput(
            label="메시지 링크 (선택)",
            default=config["link"],
            required=False
        )

        self.add_item(self.message)
        self.add_item(self.link)

    async def on_submit(self, interaction: discord.Interaction):
        # 🔹 저장
        update_guild(self.guild_id, "welcome_message", self.message.value)
        update_guild(self.guild_id, "link", self.link.value)

        # 🔹 저장된 값 다시 불러오기 (확실한 상태 확인)
        config = get_guild(self.guild_id)

        message = config["welcome_message"].replace(
            "{server}", interaction.guild.name
        )
        link = config["link"]

        # 🔹 미리보기 카드 생성
        embed = discord.Embed(
            title="연삼이 (미리보기)",
            description=message,
            color=0x5865F2
        )

        if link:
            embed.add_field(name="공지 링크", value=link, inline=False)

        # 🔹 ephemeral로 확인 메시지 + 카드 출력
        await interaction.response.send_message(
            content="수정 완료 (미리보기)",
            embed=embed,
            ephemeral=True
        )


# 🔹 버튼 View
class YeonsamView(discord.ui.View):
    def __init__(self, guild_id, is_admin):
        super().__init__()
        self.guild_id = guild_id

        if is_admin:
            self.add_item(EditButton(guild_id))


class EditButton(discord.ui.Button):
    def __init__(self, guild_id):
        super().__init__(label="메시지 수정", style=discord.ButtonStyle.primary)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EditModal(self.guild_id))


# 🔹 메인 Cog
class Yeonsam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="yeonsam", description="연삼이 소개")
    async def yeonsam(self, interaction: discord.Interaction):
        guild = interaction.guild
        config = get_guild(guild.id)

        message = config["welcome_message"].replace("{server}", guild.name)
        link = config["link"]

        embed = discord.Embed(
            title="연삼이",
            description=message,
            color=0x5865F2
        )

        if link:
            embed.add_field(name="공지 링크", value=link, inline=False)

        is_admin = interaction.user.guild_permissions.administrator

        await interaction.response.send_message(
            embed=embed,
            view=YeonsamView(guild.id, is_admin),
            ephemeral=True  # 🔹 본인만 보이게
        )


async def setup(bot):
    await bot.add_cog(Yeonsam(bot))