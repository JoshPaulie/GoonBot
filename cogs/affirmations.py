import random
from pathlib import Path

from discord.ext import commands
from discord.ext.commands import BucketType

files_assets_path = Path("helpers/love_letters")


class Affirmations(commands.Cog, name='Affirmations! ❤'):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.cooldown(1, 60, type=BucketType.user)
    @commands.command(name='cily')
    async def cily(self, ctx):
        """Reminds Conrad about your true feelings for him"""
        message = ctx.message
        possible_letters = ["Conrad, I love you",
                            "Conrad I love you",
                            "You are my best friend",
                            "I love the way you mow lawns"]
        random_emoji = random.choice(
            ['♥', '💜', '❣', '🧡', '💓', '💟', '💞', '🤍', '😻', '🥰', '😍', '💌', '❤', '💕', '🖤', '💛'])
        await ctx.send(f'{random.choice(possible_letters)} <@164600098142158848> {random_emoji}')

    @cily.error
    async def cilyError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You can tell him again in `{round(error.retry_after)}` seconds 🤗")

    @commands.cooldown(1, 60, type=BucketType.user)
    @commands.command(name='jyb')
    async def jyb(self, ctx):
        """At any moment, somewhere in the world, Justin is being based."""
        message = ctx.message
        possible_letters = ["Justin you're based",
                            "Justin, you're based.",
                            "god you're based.",
                            "Hey, I didn't know based was on the menu!",
                            "It's looking pretty based."]
        random_emoji = "😎"
        await ctx.send(f'{random.choice(possible_letters)} <@104488534936666112> {random_emoji}')

    @jyb.error
    async def jybError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You can tell him again in `{round(error.retry_after)}` seconds 🤗")


def setup(bot):
    bot.add_cog(Affirmations(bot))
