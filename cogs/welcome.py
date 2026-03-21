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
            await channel.send(f"{member.mention} {message}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))