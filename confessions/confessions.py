import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core import checks
import names

BaseCog = getattr(commands, "Cog", object)

class Confessions(BaseCog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def confess(self, ctx, *, text):
        """Sends a anonymous message to the #confession channel for people that want to vent and confess anonymously"""
        embed = discord.Embed(
            colour=discord.Colour(0x4a4a4a),
            description= text)
        embed.set_author(name= names.get_full_name() + " said:")
        embed.set_footer(text= ctx.message.channel.id)

        if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
            channel = self.bot.get_channel(467491789025050625)
            message = await channel.send(embed=embed)
        else:
            authorchannel = ctx.message.author
            await authorchannel.send("Please send your confession message via DM")
            await ctx.message.delete()

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def confessban(self, ctx, channel_id):
    
        channel = self.bot.get_channel(int(channel_id))
        print(channel)
        if channel is None:
            response = self.MESSAGE_NOT_FOUND
        else:
            server = self.bot.get_guild(220693787213561857)
            member = server.get_member(channel.recipient.id)
            await member.ban()
            authorchannel = ctx.message.author
            await authorchannel.send("User has been banned.")