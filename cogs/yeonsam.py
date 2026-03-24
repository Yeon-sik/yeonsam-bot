import discord
from discord.ext import commands

from utils.profile import update_member_nickname
from utils.storage import get_guild, update_guild


class EditModal(discord.ui.Modal):
    def __init__(self, guild_id: int):
        super().__init__(title="Edit Message")
        self.guild_id = guild_id

        config = get_guild(guild_id)

        self.message = discord.ui.TextInput(
            label="Welcome Message",
            default=config["welcome_message"],
        )
        self.link = discord.ui.TextInput(
            label="Link (Optional)",
            default=config["link"],
            required=False,
        )

        self.add_item(self.message)
        self.add_item(self.link)

    async def on_submit(self, interaction: discord.Interaction):
        update_guild(self.guild_id, "welcome_message", self.message.value)
        update_guild(self.guild_id, "link", self.link.value)

        config = get_guild(self.guild_id)
        message = config["welcome_message"].replace("{server}", interaction.guild.name)
        link = config["link"]

        embed = discord.Embed(
            title="Yeonsam Bot Preview",
            description=message,
            color=0x5865F2,
        )

        if link:
            embed.add_field(name="Announcement Link", value=link, inline=False)

        await interaction.response.send_message(
            content="Saved successfully.",
            embed=embed,
            ephemeral=True,
        )


class EditButton(discord.ui.Button):
    def __init__(self, guild_id: int):
        super().__init__(label="Edit Message", style=discord.ButtonStyle.primary)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EditModal(self.guild_id))


class ProfileButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Edit Server Profile",
            style=discord.ButtonStyle.secondary,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileModal())


class ProfileModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Edit Server Profile")

        self.nickname = discord.ui.TextInput(
            label="Nickname",
            placeholder="Enter a nickname for this server",
            max_length=32,
        )
        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        _, message = await update_member_nickname(interaction, self.nickname.value)
        await interaction.response.send_message(message, ephemeral=True)


class YeonsamView(discord.ui.View):
    def __init__(self, guild_id: int, is_admin: bool):
        super().__init__()

        if is_admin:
            self.add_item(EditButton(guild_id))

        self.add_item(ProfileButton())


class Yeonsam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="yeonsam", description="Show Yeonsam bot info")
    async def yeonsam(self, interaction: discord.Interaction):
        guild = interaction.guild
        config = get_guild(guild.id)

        message = config["welcome_message"].replace("{server}", guild.name)
        link = config["link"]

        embed = discord.Embed(
            title="Yeonsam Bot",
            description=message,
            color=0x5865F2,
        )

        if link:
            embed.add_field(name="Announcement Link", value=link, inline=False)

        is_admin = interaction.user.guild_permissions.administrator

        await interaction.response.send_message(
            embed=embed,
            view=YeonsamView(guild.id, is_admin),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Yeonsam(bot))
