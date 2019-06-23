import asyncio
import json
import aiohttp
import discord
import re
from redbot.core import commands

BaseCog = getattr(commands, "Cog", object)


class Animerequests(commands.Cog):
    """Anime Request ticket system"""

    def __init__(self, bot):
        self.bot = bot

    def description_parser(self, description):
        description = "\n".join(description.split("\n")[:5])
        if len(description) > 400:
            return description[:400] + "..."
        else:
            return description

    async def on_message(self, message):
        regexp = re.compile(r'http[s]?://')
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return
        if str(message.channel.id) != '561518060440387604':
            return
        elif message.author.bot:
            return
        elif regexp.search(message.content):
            # Query Twist.moe's JSON feed
            async with aiohttp.ClientSession() as session:
                async with session.get("https://twist.moe/feed/anime?format=json", headers={'User-Agent': "nani"}) as response:
                    datafeed = await response.json()
            kitsulink = message.content.split('/')[2]
            isanime = message.content.split('/')[3]
            botchannel = self.bot.get_channel(437190228113883136)
            if kitsulink != 'kitsu.io':
                try:
                    await message.author.send("Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                    await message.delete()
                except discord.Forbidden:
                    await botchannel.send(message.author.mention + " Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                    await message.delete()
            elif isanime != 'anime':
                try:
                    await message.author.send("Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                    await message.delete()
                except discord.Forbidden:
                    await botchannel.send(message.author.mention + " Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                    await message.delete()
            else:
                # Fetch Kitsu's API with slug
                slug = message.content.split('/')[4]
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://kitsu.io/api/edge/anime?filter%5Bslug%5D={slug}", headers={'User-Agent': "nani"}) as response:
                        kitsuapi = await response.json()

                # Get ID, Titles, Poster
                for data in kitsuapi['data']:
                    kitsuid = data['id']
                    description = data['attributes']['synopsis']
                    en_jp = data['attributes']['titles']['en_jp']
                    poster = data['attributes']['posterImage']['original']
                    episodes = data['attributes']['episodeCount']
                    status = data['attributes']['status']
                    subtype = data['attributes']['subtype']
                    title = en_jp.replace(" ", "%20")
                    title1 = title.replace("(", "%20")
                    linktitle = title1.replace(")", "%20")
                    Status = status.capitalize()
                    try:
                        en = f"({data['attributes']['titles']['en']})"
                    except:
                        en = ""

                #Loop through datafeed to check against Kitsu IDs
                for twistitem in datafeed['items']:
                    if str(twistitem['kitsu:id']) == str(kitsuid):
                        twistlink = twistitem['link']
                        embed2 = discord.Embed(title=f"{en_jp} {en}", colour=discord.Colour(0xf5a623), url=f"{twistlink}", description=self.description_parser(description))
                        embed2.set_thumbnail(url=f"{poster}")
                        embed2.add_field(name="Watch here for free:", value=f"{twistlink}")
                        try:
                            # Send embed to DM
                            await message.author.send(content="It looks like it's your lucky day, we already have the anime you requested!", embed=embed2)
                            await message.delete()
                        except discord.Forbidden:
                            await message.delete()
                            # In case DM's disabled, send in channel
                            botchannel = self.bot.get_channel(437190228113883136)
                            Message = await botchannel.send(content= message.author.mention + " It looks like it's your lucky day, we already have the anime you requested!", embed=embed2)
                            await Message.delete()
                        break
                else:
                    embed = discord.Embed(title=f"{en_jp} {en}", colour=discord.Colour(0xb8e986), url=f"https://kitsu.io/anime/{kitsuid}", description=self.description_parser(description))
                    embed.set_thumbnail(url=f"{poster}")
                    embed.set_footer(text="Requested By " + message.author.name + "#" + str(message.author.discriminator) + " (" + str(message.author.id) + ")", icon_url=message.author.avatar_url)
                    embed.add_field(name="Episodes:", value=f"{episodes}", inline=True)
                    embed.add_field(name="Status, Type:", value=f"{Status} - {subtype}", inline=True)
                    embed.add_field(name="Links:", value=f"[Nyaa](https://nyaa.si/?f=0&c=1_2&q={linktitle}&s=seeders&o=desc), [AnimeTosho](https://animetosho.org/search/?q={linktitle})", inline=True)
                    embed.add_field(name="Kitsu Slug:", value=f"`{slug}`", inline=True)
                    requestticket = await message.channel.send(embed=embed)
                    await requestticket.add_reaction(emoji="🕒")
                    await requestticket.add_reaction(emoji="✅")
                    await requestticket.add_reaction(emoji="⛔")
                    await message.delete()
        else:
            try:
                await message.author.send("Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                await message.delete()
            except discord.Forbidden:
                await botchannel.send(message.author.mention + " Invalid request. please make sure you're only sending a kitsu anime link. E.g. `https://kitsu.io/anime/death-note`")
                await message.delete()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        uploads = self.bot.get_channel(380499380786167819)
        Message = await channel.get_message(id=payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        Member = guild.get_member(payload.user_id)
        role = discord.utils.find(lambda r: r.name == 'AT Team', guild.roles)
        if str(payload.channel_id) != '561518060440387604':
            return
        elif Member.bot:
            return
        elif role not in Member.roles:
            return
        else:
            if str(payload.emoji) == "🕒":
                embed = discord.Embed(title=Message.embeds[0].title, colour=discord.Colour(0xf8e71c), url=Message.embeds[0].url, description=Message.embeds[0].description)
                embed.set_thumbnail(url=Message.embeds[0].thumbnail.url)
                embed.set_author(name="In Progress")
                embed.set_footer(text=Message.embeds[0].footer.text, icon_url=Message.embeds[0].footer.icon_url)
                embed.add_field(name=Message.embeds[0].fields[0].name, value=Message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=Message.embeds[0].fields[1].name, value=Message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=Message.embeds[0].fields[2].name, value=Message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=Message.embeds[0].fields[3].name, value=Message.embeds[0].fields[3].value, inline=True)
                await Message.edit(embed=embed)
            if str(payload.emoji) == "✅":
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://twist.moe/feed/anime?format=json", headers={'User-Agent': "nani"}) as response:
                        datafeed = await response.json()
                url = Message.embeds[0].url
                kitsuid = url.split('/')[4]

                for twistitem in datafeed['items']:
                    if str(twistitem['kitsu:id']) == str(kitsuid):
                        twistlink = twistitem['link']
                        print(twistlink)
                        em = discord.Embed(title=Message.embeds[0].title, colour=discord.Colour(0x1c1f22), url=f"{twistlink}", description=Message.embeds[0].description)
                        em.set_image(url=Message.embeds[0].thumbnail.url)
                        em.set_footer(text="Uploaded By " + Member.name + "#" + str(Member.discriminator), icon_url= Member.avatar_url)
                        await uploads.send(embed=em)
                        await Message.delete()
                        break
                else:
                    await Member.send("Looks like you haven't Uploaded the anime to the database yet, try again when you do.")
            if str(payload.emoji) == "⛔":
                botchannel = self.bot.get_channel(437190228113883136)
                embed2 = discord.Embed(title=Message.embeds[0].title, colour=discord.Colour(0xd0021b), url=Message.embeds[0].url, description=Message.embeds[0].description)
                embed2.set_thumbnail(url=Message.embeds[0].thumbnail.url)
                embed2.set_author(name="Request Denied")
                footer = Message.embeds[0].footer.text
                userid = footer[footer.find("(")+1:footer.find(")")]
                denieduser = guild.get_member(int(userid))
                try:
                    await denieduser.send(embed=embed2, content="Your anime request has been denied by " + Member.mention + "\nCommon reasons would be that:\n • We couldn't find a source for the anime.\n • The sources we found don't live up to our standards.\n • The anime has too many episodes.\n\nIf you happen to find a source yourself to provide or disagree with this choice, please contact the responsible content manager that denied your request.")
                    await Message.delete()
                except discord.Forbidden:
                    await botchannel.send(embed=embed2, content= denieduser.mention + " Your anime request has been denied by " + Member.name + "#" + str(Member.discriminator) + "\nCommon reasons would be that:\n • We couldn't find a source for the anime.\n • The sources we found don't live up to our standards.\n • The anime has too many episodes.\n\nIf you happen to find a source yourself to provide or disagree with this choice, please contact the responsible content manager that denied your request.")
                    await Message.delete()

