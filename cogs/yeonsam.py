import discord
from discord.ext import commands
from utils.storage import get_guild, update_guild

class EditModal(discord.ui.Modal):
    def __init__(self, guild_id):
        super().__init__(title="메시지 수정")
        self.guild_id = guild_id

        self.message = discord.ui.TextInput(
            label="출력 메시지",
            default="Welcome to {server}"
        )

        self.link = discord.ui.TextInput(
            label="메시지 링크 (선택)",
            required=False
        )

        self.add_item(self.message)
        self.add_item(self.link)

    async def on_submit(self, interaction: discord.Interaction):
        update_guild(self.guild_id, "welcome_message", self.message.value)
        update_guild(self.guild_id, "link", self.link.value)

        await interaction.response.send_message("수정 완료", ephemeral=True)


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
        modal = EditModal(self.guild_id)
        await interaction.response.send_modal(modal)


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
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Yeonsam(bot))