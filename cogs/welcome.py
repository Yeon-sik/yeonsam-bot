member = interaction.guild.get_member(interaction.user.id)

try:
    await member.edit(nick=self.nickname.value)