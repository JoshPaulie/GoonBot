import discord
import pandas as pd
from discord.ext import commands


def make_df():
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_state.csv')
    data_us = df[df['Country_Region'] == "US"].set_index('Province_State')
    return data_us


class CoronaVirus(commands.Cog, name="Covid 😷"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='virus', aliases=['covid', 'corona', 'covid19', 'thevarus', 'varus'])
    async def virus(self, ctx, state: str = None):
        """Covid Data in Goon States

        Syntax: `.virus (ok/az/md/ca/none)`
        *No state abbreviation returns all 4 stats*"""

        goon_cases = 1
        goon_mortality_rate = 100  # if i catch the virus and my lungs crap out PLEASE update this for me, we strive
        # for accuracy

        embed = discord.Embed(title='JHU Live Stats', description=f'A medley of stats, stay safe my friends 🤗')
        data = make_df()
        states = []

        if state is not None:
            if state.lower() in ["ok", "oklahoma"]:
                states.append("Oklahoma")
            elif state.lower() in ["az", "arizona"]:
                states.append("Arizona")
            elif state.lower() in ["md", "maryland"]:
                states.append("Maryland")
            elif state.lower() in ["ca", "california"]:
                states.append("California")
        else:
            states.extend(['Oklahoma', 'Arizona', 'California', 'Maryland'])

        for state in states:
            confirmed_cases = data.loc[state, 'Confirmed']
            deaths = data.loc[state, 'Deaths']
            recovered = data.loc[state, 'Recovered']
            mortality_rate = round(data.loc[state, 'Mortality_Rate'], 2)

            embed.add_field(name=f'{state}',
                            value=f'Cases: **{confirmed_cases:,d}**\nDeaths & Recoveries: **{deaths:,d}** & **{str(recovered).strip(".0")}** '
                                  f'\nVirus W/R: **{mortality_rate}%**',
                            inline=False)

        embed.set_footer(text=f'Goon Cases: {goon_cases} | Goon W/R: {goon_mortality_rate}% 😎')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CoronaVirus(bot))
