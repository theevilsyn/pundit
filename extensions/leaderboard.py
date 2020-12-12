import logging
from asyncio import sleep as asleep

import discord
from core.pundit.pundit import PUNDIT, Pundit
from discord.ext import commands, tasks
from discord.ext.commands import errors as discorderr
from discord.utils import get

pundit = Pundit()

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def leaderboard(self, ctx, check):
        """
        Displays the scoreboard
        Dont run this command unless you know the consequences it may create
        """
        if(check == "punditisgreat"):self.start()
        else:return await ctx.send("Nah bro!!")

    async def start(self, *args):
        leaderChnl = get(
            get(
                self.bot.get_guild(id=PUNDIT['server']).categories, name='announcements'
            )
            .channels,
            name='leaderboard'
        )
        boardPresent = any(
            msg.author == self.bot.user and any(msg.embeds)
            for msg in await leaderChnl.history().flatten()
        )
        if(not boardPresent):
            board = pundit.leaderboard(count=15)
            leaderboard=discord.Embed(
                title="Leaderboard",
                description="Leader board for the recruitment tasks",
                color=0xff0000
            )
            leaderboard.set_footer(
                text="Note: This is an automatically generated report by pundit."
            )
            leaderboard.add_field(
                name="Rank",
                value="\n".join(list(map(str, list(range(1,len(board)+1))))),
                inline=True
            )
            leaderboard.add_field(
                name="User",
                # value="\n".join(list(map(lambda x: str(self.bot.get_user(int(x[0]))).split("#")[0], board))),
                value = await self.get_name(board),
                inline=True
            )
            leaderboard.add_field(
                name="Score",
                value="\n".join(list(map(lambda x: str(x[1]), board))),
                inline=True
            )
            if(len(board)>=1):
                await leaderChnl.send(embed=leaderboard)
            self.bot.loop.create_task(self.update_board(leaderChnl))
        else:self.bot.loop.create_task(self.update_board(leaderChnl))
    
    #latest get name function (0_<)
    async def get_name(self,board):
        server = self.bot.get_guild(id=PUNDIT['server'])
        names = ['']*len(board)
        for tag,ids in enumerate(board):
            names[tag] = await server.fetch_member(ids[0])
            names[tag] = names[tag].name
        names = "\n".join(names)
        return names


    async def update_board(self, leaderChnl):
        while not self.bot.is_closed():
            boardPresent = False
            async for msg in leaderChnl.history():
                    if(msg.author == self.bot.user and any(msg.embeds)):
                        message = msg;boardPresent = True
            board=pundit.leaderboard(count=15)
            newembed=discord.Embed(
                title="Leaderboard",
                description="Leader board for the recruitment tasks",color=0xff0000
            )
            newembed.set_footer(
                text="Note: This is an automatically generated report by pundit."
            )
            newembed.add_field(
                name="Rank",value="\n".join(
                    list(
                        map(
                            lambda key: key,
                            list(
                                map(
                                    str,
                                    list(range(1,len(board)+1))
                                )
                            )  
                        )
                    )
                ),inline=True
            )
            newembed.add_field(
                name="User",
                # value="\n".join(
                #     list(
                #         map(
                #             lambda key: key,
                #             list(
                #                 map(
                #                     lambda x: str(self.bot.get_user(int(x[0]))).split("#")[0],
                #                     board
                #                 )
                #             )
                #         )
                #     )
                # ),
                value = await self.get_name(board),
                inline=True
            )
            newembed.add_field(
                name="Score",
                value="\n".join(
                    list(
                        map(
                            lambda key: key,
                            list(
                                map(
                                    lambda x: str(x[1]),
                                    board
                                )
                            )
                        )
                    )
                ),
                inline=True
            )
            if(boardPresent):
                try:
                    for oldfield, newfield in zip(message.embeds[0].fields, newembed.fields):
                        if(oldfield.value!=newfield.value):
                            await message.edit(embed=newembed)
                except discord.errors.NotFound:
                    await leaderChnl.send(embed=newembed)    
            else:
                if(len(board)>=1):
                    await leaderChnl.send(embed=newembed)
            await asleep(1)

def setup(bot):
    bot.add_cog(Leaderboard(bot))