import signal
import logging
from time import sleep

import discord
from discord.utils import get
from discord.ext import (
    flags,
    commands
)
from discord.ext.commands import errors as discorderr

from core.pundit.pundit import (
    PUNDIT,
    STORAGE,
    Pundit,
)
from core.pundit.helpers import timeout_handler


class Plagiarism(commands.Cog):
    # todo replace all bot instances with client
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_any_role(*(PUNDIT['adminroles']))
    async def moss(self, ctx):
        """
        Collection of commands for the plagiarism reports
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Invalid command passed.  Use !help."
            )
        self.pundit = Pundit()

    @moss.command(pass_context=True)
    async def bytask(self, ctx, task):
        """
        Run a plagiarism check for all the submissions on the task given
        """
        server = ctx.bot.get_guild(id=int(PUNDIT['server']))
        if(get(server.categories, id=get(server.channels, id=ctx.channel.id).category_id).name not in PUNDIT['admincategories']):
            return await ctx.send(
                "Sorry, not here!!!, go to some admin-only channel!!"
            )
    
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        try:
            mossret = self.pundit.plagCheck(task=task)
            sleep(7) # to prevent raising exception when control flow passed from here
        except Exception:
            try:
                assert mossret
            except NameError:
                mossret = (False,"Request for Moss timed out!!")

        if("No files" in mossret[1]):
            return await ctx.send(f"No submissions in the task {task} yet!!")
        if mossret[0]:
            mossret = mossret[1].split('\n')
            for result in mossret:
                report = result.split(' * ')
                await ctx.send(embed = self.createEmbed(
                    description= task,
                    names = [report[0],report[2]],
                    scores= report[-1]
                ))
        else:    
            return await ctx.send(f"Here's the plagiarism report for the task {task}\n{mossret[1]} !!")

    @moss.command()
    async def bytasks(self, ctx, *params):
        """
        Run a plagiarism check for all the submissions on the tasks given
        """
        server = ctx.bot.get_guild(id=int(PUNDIT['server']))
        if(get(server.categories, id=get(server.channels, id=ctx.channel.id).category_id).name not in PUNDIT['admincategories']):
            return await ctx.send(
                "Sorry, not here!!!, go to some admin-only channel!!"
            )
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(6)
        try:
            mossret = self.pundit.plagCheck(tasks=list(params))
            sleep(7) # to prevent raising exception when control flow passed from here
        except Exception:
            try:
                assert mossret
            except NameError:
                mossret = {
                    'python': 'timeout',
                    'c': 'timeout'
                }

        return await ctx.send(f"Report for Python tasks in the given: {mossret['python']}\nReport for C tasks in the given: {mossret['c']}")

    @moss.command()
    async def bylanguage(self, ctx, language):
        """
        Run a plagiarism check for all the submissions for the tasks in the given programming language
        """
        server = ctx.bot.get_guild(id=int(PUNDIT['server']))
        if(get(server.categories, id=get(server.channels, id=ctx.channel.id).category_id).name not in PUNDIT['admincategories']):
            return await ctx.send(
                "Sorry, not here!!!, go to some admin-only channel!!"
            )

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(18)
        try:
            mossret = self.pundit.plagCheck(language=language)
            sleep(20) # to prevent raising exception when control flow passed from here
        except Exception:
            try:
               assert mossret
            except NameError:
                # mossret is not set
                mossret = "Timeout reaching moss!" 

        if("No files" in mossret):
            return await ctx.send(f"No submissions in the {language} yet!!")
        return await ctx.send(f"Here's the report for tasks in {language}\n{mossret}")

    @moss.command()
    async def byusers(self, ctx, *params):
        """
        Command to compare a set of tasks for a set of users
        !moss byusers --users user1 user2 user3 --tasks task1 task2 task3
        """
        users = params[params.index('--users')+1:params.index('--tasks')]
        tasks = params[params.index('--tasks')+1:]

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(6)
        try:
            mossret = self.pundit.plagCheck(
                users=list(users), usertasks=list(tasks))
            sleep(7) # to prevent raising exception when control flow passed from here
        except Exception:
            print("Timeout")
            try:
                assert mossret
            except NameError:
                mossret = {
                'python': 'timeout',
                'c': 'timeout'
                }

        return await ctx.send(f"Report for Python tasks in the given: {mossret['python']}\nReport for C tasks in the given: {mossret['c']}")
    
    def createEmbed(self,description = "",names = [] ,scores = ''):
        report = discord.Embed(
            title="Plagarirsm Report",
            description=description,
            color=0xff0000
        )
        if(names):
            report.add_field(
                name="Candidates",
                value="""```1.{}``` 
                ```2.{}```""".format(names[0],names[1]),
            )
        if(scores):
            report.add_field(
                name = "Scores",
                value = "``` {} ```".format(scores)
            )
        return report

def setup(bot):
    bot.add_cog(Plagiarism(bot))
