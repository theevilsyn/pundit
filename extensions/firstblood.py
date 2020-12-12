import logging
from asyncio import sleep as asleep
from datetime import datetime

import discord
from core.pundit.pundit import PUNDIT, Pundit
from discord.ext import commands, tasks
from discord.ext.commands import errors as discorderr
from discord.utils import get

pundit = Pundit()


class Firstbloods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_name(self,board):
        server = self.bot.get_guild(id=PUNDIT['server'])
        names = ['']*len(board)
        for tag,ids in enumerate(board):
            names[tag] = await server.fetch_member(ids[0])
            names[tag] = names[tag].name
        names = "\n".join(names)
        return names

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def firstblood(self, ctx, check):
        """
        Displays the scoreboard
        Dont run this command unless you know the consequences it may create
        """
        if(check == "punditisgreat"):
            self.start()
        else:
            return await ctx.send("Nah bro!!")

    async def start(self, *args):
        bloodChnl = get(
            get(
                self.bot.get_guild(
                    id=PUNDIT['server']).categories, name='announcements'
            )
            .channels,
            name='firstbloods'
        )
        boardPresent = any(
            msg.author == self.bot.user and any(msg.embeds)
            for msg in await bloodChnl.history().flatten()
        )
        if(not boardPresent):
            bloods = pundit.firstbloods()
            bloodboard = discord.Embed(
                title="Firstbloods",
                description="Firstblood details for the recruitment tasks",
                color=0xff0000
            )
            bloodboard.set_footer(
                text="Note: This is an automatically generated report by pundit."
            )
            bloodboard.add_field(
                name="Which?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(bloods.keys())))),
                inline=True
            )
            bloodboard.add_field(
                name="Who?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(map(lambda task: (str(task[0]).split(
                    "#")[0] if type(task) is tuple else "None Yet :/"), list(bloods.values())))))),
                inline=True
            )
            bloodboard.add_field(
                name="When?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(map(lambda task: (datetime.fromtimestamp(task[1]).strftime(
                    "%b %d, %H:%M:%S") if type(task) is tuple else "Soon Enough!!"), list(bloods.values())))))),
                inline=True
            )
            await bloodChnl.send(embed=bloodboard)
            self.bot.loop.create_task(self.update_board(bloodChnl))
        else:
            self.bot.loop.create_task(self.update_board(bloodChnl))

    async def update_board(self, bloodChnl):
        while not self.bot.is_closed():
            boardPresent = False
            async for msg in bloodChnl.history():
                if(msg.author == self.bot.user and any(msg.embeds)):
                    message = msg
                    boardPresent = True
            bloods = pundit.firstbloods()
            newembed = discord.Embed(
                title="Leaderboard",
                description="Firstblood details for the recruitment tasks", color=0xff0000
            )
            newembed.set_footer(
                text="Note: This is an automatically generated report by pundit."
            )
            newembed.add_field(
                name="Which?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(bloods.keys())))),
                inline=True
            )
            newembed.add_field(
                name="Who?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(map(lambda task: (str(task[0]).split(
                    "#")[0] if type(task) is tuple else "None Yet :/"), list(bloods.values())))))),
                inline=True
            )
            newembed.add_field(
                name="When?",
                value="\n".join(list(map(lambda key: f"```{key}```", list(map(lambda task: (datetime.fromtimestamp(task[1]).strftime(
                    "%b %d, %H:%M:%S") if type(task) is tuple else "Soon Enough!!"), list(bloods.values())))))),
                inline=True
            )
            if(boardPresent):
                try:
                    for oldfield, newfield in zip(message.embeds[0].fields, newembed.fields):
                        if(oldfield.value != newfield.value):
                            await message.edit(embed=newembed)
                except discord.errors.NotFound:
                    await bloodChnl.send(embed=newembed)
            else:
                await bloodChnl.send(embed=newembed)
            await asleep(1)


def setup(bot):
    bot.add_cog(Firstbloods(bot))
