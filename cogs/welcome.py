from discord.ext import commands
import discord
from utils.storage import get_guild


class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ProfileButton())


class ProfileButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="서버 프로필 변경", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileModal())


class ProfileModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="서버 프로필 변경")

        self.nickname = discord.ui.TextInput(
            label="닉네임",
            placeholder="새 닉네임 입력"
        )

        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.user.edit(nick=self.nickname.value)

            await interaction.response.send_message(
                f"닉네임이 '{self.nickname.value}'로 변경됨",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "권한 부족: 봇 역할을 위로 올려야 함",
                ephemeral=True
            )


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = get_guild(member.guild.id)

        message = config["welcome_message"].replace("{server}", member.guild.name)

        channel = member.guild.system_channel

        if channel:
            embed = discord.Embed(
                title="환영합니다",
                description=f"{member.mention} {message}",
                color=0x5865F2
            )

            await channel.send(
                embed=embed,
                view=WelcomeView()
            )


async def setup(bot):
    await bot.add_cog(Welcome(bot))