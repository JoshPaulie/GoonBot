import datetime
from pathlib import Path

import discord
from discord.ext import commands
from helpers.countdown_dates.major_events import birthdays, major_events

files_assets_path = Path("helpers")
now = datetime.datetime.now()  # ! redundant ⤵
today_date = datetime.datetime.date(now)


def calc_age(today, birthday):
    return today.year - birthday.year


def how_long_until(date):
    remaining = date - today_date
    return remaining


class MajorEvents(commands.Cog, name="Major Events! 📅"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='birthday', aliases=['bday', 'holiday', 'event', 'events', 'majorevents', 'holidays'])
    async def birthday(self, ctx):
        """Countdown to major events!"""
        message = ctx.message
        birthday_today = False
        holiday_today = False

        embed_today_events = discord.Embed(title="It's a big day!")

        for bday, person in birthdays.items():
            if bday.day == today_date.day and bday.month == today_date.month:
                special_guy = ctx.guild.get_member(person)
                embed_today_events.add_field(name=f"It's {special_guy.mention}'s birthday!",
                                             value=f"They turn {calc_age(today_date, bday)} today!")
                birthday_today = True

        for event_date, event in major_events.items():
            if event_date.day == today_date.day and event_date.month == today_date.month:
                embed_today_events.add_field(name=f"Today is {event}", value="🥳")
                holiday_today = True

        if birthday_today is True or holiday_today is True:
            await ctx.send(embed=embed_today_events)

        if birthday_today is False and holiday_today is False:
            embed = discord.Embed(title="Birthdays & Major Events! 📅")
            for bday, person in birthdays.items():
                special_guy = ctx.guild.get_member(person)
                days_left = how_long_until(bday).days
                if days_left >= 1:
                    embed.add_field(name=special_guy.name, value=f"{days_left} days remaining!", inline=True)
            for event_date, event in major_events.items():
                days_left = how_long_until(event_date).days
                if days_left >= 1:
                    embed.add_field(name=event, value=f"{days_left} days remaining!", inline=True)
            embed.colour = ctx.author.colour

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MajorEvents(bot))
