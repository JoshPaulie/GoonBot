import random
from pathlib import Path

import discord
from discord.ext import commands
from googletrans import Translator

files_assets_path = Path("helpers")


class LanguageTools(commands.Cog, name="Language Tools! 💬"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Looks for speech emojis
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Checks for emoji adds"""
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name
        translator = Translator()

        if emoji == "💬":
            try:
                async with channel.typing():
                    msg_in_en = translator.translate(message.content)
                embed = discord.Embed(title="Quick Translate!",
                                      description=f"Original language: {msg_in_en.src}")
                embed.add_field(name=f'{message.author.name}:',
                                value=f"{msg_in_en.text}", inline=True)
                embed.set_footer(text="Powered by Google Translate\nShorter messages can be less accurate.",
                                 icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/480px-Google_Translate_logo.svg.png")
                embed.colour = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255),
                                                       random.randint(0, 255))

                await channel.send(embed=embed)
            except:
                error_msg = await channel.send("💀 The Google Translate library has failed us again.\n"
                                               "ℹ **You can try translating again, no promises it works**")
                await error_msg.delete(delay=5)
                await message.clear_reactions()

    @commands.command(name="translate")
    async def translate(self, ctx):
        """How to translate messages in the discord to English"""
        message = ctx.message
        embed = discord.Embed(title="How to Translate Any Message",
                              description="React with any of the following emotes to translate a message to English")
        embed.add_field(name="Translate Emotes", value="`💬`")
        embed.set_footer(text="")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LanguageTools(bot))
