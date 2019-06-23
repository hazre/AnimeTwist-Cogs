import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core import checks

import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import aiohttp
import json

BaseCog = getattr(commands, "Cog", object)

class Suggestions(BaseCog):
    """Anime Twist Suggestions"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def suggest(self, ctx, *, text):
        """Don't worry we'll add new things, just suggest whatever it's in your mind."""
        embed = discord.Embed(
            colour=discord.Colour(0x4a4a4a),
            description= text)
        attach = ctx.message.attachments

        url = ""
        image_attachments = [u for u in text.split(" ") if u.endswith((".png", ".jpg", ".jpeg", ".gif"))]
        if attach:
            url = attach[0].url
        elif len(image_attachments) >= 1:
            url = image_attachments[0]

        embed.set_image(url= url)
        embed.set_author(name= "Suggestion from " + ctx.message.author.name + "#" + ctx.message.author.discriminator, icon_url= ctx.message.author.avatar_url)
        embed.set_footer(text= ctx.message.author.id)

        channel = self.bot.get_channel(548164833623932933)
        message = await channel.send(embed=embed)
        await message.add_reaction(emoji="✔")
        await message.add_reaction(emoji="❌")
        if isinstance(ctx.message.channel, discord.TextChannel):
                await ctx.message.delete()

    async def on_message(self, message):
        role = discord.utils.find(lambda r: r.name == 'AT Team', message.guild.roles)
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        if str(message.channel.id) != '435922449066885121':
            return
        elif message.author.bot:
            return
        elif role in message.author.roles:
            return
        else:
            embed = discord.Embed(
            colour=discord.Colour(0x4a4a4a),
            description= message.content)
            attach = message.attachments

            url = ""
            image_attachments = [u for u in message.content.split(" ") if u.endswith((".png", ".jpg", ".jpeg", ".gif"))]
            if attach:
                url = attach[0].url
            elif len(image_attachments) >= 1:
                url = image_attachments[0]

            embed.set_image(url= url)
            embed.set_author(name= "Suggestion from " + message.author.name + "#" + message.author.discriminator, icon_url= message.author.avatar_url)
            embed.set_footer(text= message.author.id)

            channel = message.channel
            Message = await channel.send(embed=embed)
            await Message.add_reaction(emoji="✔")
            await Message.add_reaction(emoji="❌")
            await message.delete()