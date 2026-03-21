from discord.ext import commands
from utils.storage import get_guild

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

class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ProfileButton())

async def setup(bot):
    await bot.add_cog(Welcome(bot))