import discord
from discord.ext import commands
from utils.storage import get_guild


# 🔹 닉네임 변경 버튼
class ProfileButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="서버 프로필 변경", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileModal())


# 🔹 닉네임 입력 Modal
class ProfileModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="서버 프로필 변경")

        self.nickname = discord.ui.TextInput(
            label="닉네임",
            placeholder="새 닉네임 입력",
            max_length=32
        )

        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)

        try:
            await member.edit(nick=self.nickname.value)

            await interaction.response.send_message(
                f"닉네임이 '{self.nickname.value}'로 변경됨",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ 권한 부족: 봇 역할이 더 위에 있어야 합니다.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ 오류 발생: {e}",
                ephemeral=True
            )


# 🔹 환영 메시지에 붙는 View
class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 지속 유지
        self.add_item(ProfileButton())


# 🔹 메인 Cog
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
                title="🎉 환영합니다!",
                description=f"{member.mention}\n{message}",
                color=0x5865F2
            )

            await channel.send(
                embed=embed,
                view=WelcomeView()
            )


async def setup(bot):
    await bot.add_cog(Welcome(bot))