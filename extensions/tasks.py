import sys
import discord
from asyncio import *
from operator import concat
from functools import reduce
from discord.utils import get
from discord.ext import (
    flags,
    commands,
)
from discord.channel import DMChannel
from discord.ext.commands import errors as discorderr

from core.validator.validator import Validator
from core.pundit.helpers import (
    submission,
    plagCheck,
    isUrl,
)
from core.pundit.pundit import (
    Pundit as _Pundit,
    TASKS,
    PUNDIT,
    STORAGE,
)
from extensions.plagiarism import Plagiarism
from utils.progressbar import draw_bar

pundit = _Pundit()
CHALLENGE_CATEGORIES = list(
    set(reduce(concat, list(map(lambda task: TASKS[task]['tags'], TASKS)))))


class Pundit(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.plagiarism = Plagiarism(client)

    @commands.group()
    async def tasks(self, ctx):
        """
        Collection of commands related to tasks
        """
        if(isinstance(ctx.channel, DMChannel)):
            pass
        else:
            self.guild = ctx.guild
            self.gid = ctx.guild.id
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Invalid command passed.  Use !help."
            )

    # Commands
    @tasks.command()
    async def help(self, ctx):
        """
        Shows this message
        """
        await ctx.send(
            "Nah, it's `!help tasks`"
        )

    @tasks.command(pass_context=True)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def submit(self, ctx, link):
        if(isinstance(ctx.channel, DMChannel)):
            if(isUrl(link)):
                pass
            else:
                await ctx.send("Please give a proper link!!")
                return
            submission_id = submission(ctx.author.id, STORAGE)
            await ctx.send(
                f"Thanks for your submission {ctx.author.mention}, here's your submission ID, `{submission_id}` keep it safe.\nPlease hangout for sometime and come again while I validate your tasks!!"
            )
            report = pundit.evaluate(ctx.author, link, submission_id)
            server = self.client.get_guild(id=PUNDIT['server'])
            user = await server.fetch_member(ctx.author.id)
            # user = server.get_member(ctx.author.id)
            role = get(user.roles, name=report['roletobe'])
            if((not role) and (report['roletobe'])):
                roletobe = get(server.roles, name=report['roletobe'])
                await user.add_roles(roletobe)
                await ctx.send("Yayyy!!! You've got upgrade to next level, check out for the new tasks. Good Luck!!")
            else:
                pass

            embedreport = discord.Embed(
                title="Pundit's Report [Submission No. {subs}]".format(
                    subs=len(submission_id.submissions)+1),
                description=f"Here's the report for the tasks that {str(user)} submitted just now",
                color=0x00ff00,
            )
            embedreport.set_footer(
                text=f"This is an automatically generated report for the submisison by pundit. Contact any admin in case of issues.")

            if(type(report) == tuple):
                return await ctx.send(report[1])
            fails = []
            for task in report['tasks']:
                if(type(report['tasks'][task]) == tuple):
                    # flag evaluated challenge
                    if(report['tasks'][task][0] == False):
                        try:
                            name='```'+TASKS[task]['name']+'```'
                        except KeyError:
                            name='```'+task+'```'
                        embedreport.add_field(
                            name=name,
                            value='`=========================================================`',
                            inline=False,
                        )
                        embedreport.add_field(
                            name="Status",
                            value="Failed",
                        )
                        embedreport.add_field(
                            name="Remarks",
                            value=report['tasks'][task][1]
                        )
                    else:
                        embedreport.add_field(
                            name='`'+TASKS[task]['name']+'`',
                            value='`=========================================================`',
                            inline=False,
                        )
                        embedreport.add_field(
                            name="Status",
                            value="Passed",
                        )
                        embedreport.add_field(
                            name="Remarks",
                            value="None",
                        )
                else:
                    if(report['tasks'][task]['failed']):
                        failed_cases = discord.Embed(
                            title=f"Failed testcases for task {repr(TASKS[task]['name'])}",
                            description='',
                            color=0xff0000,
                        )
                        failcases = report['tasks'][task]['failed']
                        for case in range(len(failcases)):
                            failed_cases.add_field(
                                name=f"`Testcase {case+1}`",
                                value="`===================================`",
                                inline=False,
                            )
                            failed_cases.add_field(
                                name="Input",
                                value=
                                ('```\n\n' +
                                list(failcases[case][3].keys())[0]+'```'
                                if failcases[case][2] == 'wrong'
                                else "```" + failcases[case][3] + "```")[:1020]
                            )
                            failed_cases.add_field(
                                name="Output",
                                value=
                                ('```\n\n' +
                                failcases[case][3][list(
                                    failcases[case][3].keys())[0]]+'```'
                                if failcases[case][2] == 'wrong'
                                else f'```{failcases[case][2]}```')[:1020]
                            )
                        fails.append(failed_cases)
                        embedreport.add_field(
                            name='`'+TASKS[task]['name']+'`',
                            value='`=========================================================`',
                            inline=False,
                        )
                        embedreport.add_field(
                            name="Status", 
                            value="Failed",
                        )
                        embedreport.add_field(
                            name="Remarks",
                            value="Failed at one or more testcases",
                        )
                    else:
                        embedreport.add_field(
                            name='`'+TASKS[task]['name']+'`',
                            value='`=========================================================`',
                            inline=False,
                        )
                        embedreport.add_field(
                            name="Status",
                            value="Passed",
                        )
                        embedreport.add_field(
                            name="Remarks",
                            value="None",
                        )
                    pass
            await ctx.send(embed=embedreport)
            [await ctx.send(embed=fail) for fail in fails]

            await get(get(server.categories, name='admins').channels, name="task-submissions").send(
                f"**[New Submission]** User: `{str(user)}`"
            )
            await get(get(server.categories, name='admins').channels, name="task-submissions").send(embed=embedreport)
            [await get(get(server.categories, name='admins').channels, name="task-submissions").send(embed=fail) for fail in fails]

            return

            # comment the above
            await get(get(server.categories, name='admins').channels, name="pundit-reports").send(
                f"@here there's a new submission by a user ({str(user)}) for the tasks `{', '.join(list(report['tasks'].keys()))}`."
                "\nPlease find the attached plagiarism reports for the tasks submitted.\n"
            )
            # mossrets = []
            # for task in list(report['tasks'].keys()):
            #     print(f"checking task {task}")
            #     mossrets.append(f'**{task}**: {await plagCheck(pundit, task=task)}')
            try:

                await get(get(server.categories, name='admins').channels, name="pundit-reports").send(

                    # "\n\n".join(mossrets)                

                    "\n\n".join(
                        list(
                            map(
                                lambda task: f'**{task}**: {plagCheck(pundit, task=task)}',
                                list(report['tasks'].keys())
                            )
                        )
                    )
                )
            except Exception:
                pass
        else:
            return await ctx.send("This feature is only for DMs")

    @commands.group()
    async def stats(self, ctx):
        """
        Collection of commands for player statistics
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command passed. Use `!help`.")

    @stats.command()
    async def me(self, ctx, *params):
        """
        Displays your tasks status. Use --style <N> to change text format.
        """
        style = 5
        for p in params:
            try:
                if(p == "--style"):
                    style = int(params[params.index(p)+1])
            except ValueError:
                await ctx.send("wtf are you saying....")
                return

        categories_solved = {k: 0 for k in CHALLENGE_CATEGORIES}
        solvedbyuser = pundit.solvedbyuser(ctx.author.id)
        for task in solvedbyuser:
            categories_solved[TASKS[task]['tags'][0]] += 1

        total = sum(categories_solved.values())
        mx = max(categories_solved.values())

        to_ret = "\n".join(
            [
                f"{draw_bar(categories_solved[k], mx, style=style)} {k.upper()} x{categories_solved[k]}"
                for k in CHALLENGE_CATEGORIES
            ]
        )
        to_ret = "Total Score : {0} \nTotal {1} Challenge(s) Solved: {2}\n\n".format(pundit.getScore(ctx.author.id)[0],total, ', '.join(solvedbyuser)) + to_ret

        preambles = [
            "👶 You are just a baby",  # 0-5 solved
            "👍 Man! You are hardcore",  # 6-10 solved
            "🐐👑 Legend!",  # 10+ solved
        ]
        p_choice = preambles[min(int(total / 5), len(preambles) - 1)]
        await ctx.send(f"{p_choice}\n```CSS\n{to_ret}```")

    @stats.command()
    @commands.has_any_role(*(PUNDIT['adminroles']))
    async def user(self, ctx, *params):
        """
        Displays a particular person's tasks status. Use --style <N> to change text format. Tag the person or just use --name <username#discriminator>  or --userid 538775284644577XXX | Only for admins
        """
        style = 5
        userid = 1111111111111
        for p in params:
            try:
                if(p == "--style"):
                    style = int(params[params.index(p)+1])

                if(p == "--name"):
                    name = params[params.index(p)+1]
                    userid = ''
                    if(name.startswith("<@!")):
                        del name
                        userid = ctx.message.mentions[1].id if ctx.message.mentions[0].name == 'pundit' else ''
                if(p == "--userid"):
                    userid = params[params.index(p)+1]
            except ValueError:
                await ctx.send("wtf are you saying....")
                return
        categories_solved = {k: 0 for k in CHALLENGE_CATEGORIES}
        try:
            if(name == ''):
                return await ctx.send('No user selected/tagged!!')
        except NameError:
            name=None
        if(userid == '' and name == '' and '--user' in params):
            return await ctx.send('No user selected/tagged!!')
        if(userid != ''):
            name = ''
        solvedbyuser = pundit.solvedbyuser(param = name if name != '' else int(userid))
        if(solvedbyuser is None):
            return await ctx.send("No such user registered!!!")
        if(not len(solvedbyuser)):
            await ctx.send("No solves yet!!")
        for task in solvedbyuser:
            categories_solved[TASKS[task]['tags'][0]] += 1

        total = sum(categories_solved.values())
        mx = max(categories_solved.values())

        to_ret = "\n".join(
            [
                f"{draw_bar(categories_solved[k], mx, style=style)} {k.upper()} x{categories_solved[k]}"
                for k in CHALLENGE_CATEGORIES
            ]
        )
        to_ret = "Total Score : {0} \nTotal {1} Challenge(s) Solved: {2}\n\n".format(
            pundit.getScore(userid,name)[0],
            total, ', '.join(solvedbyuser)) + to_ret

        preambles = [
            "👶 Just a baby",  # 0-5 solved
            "👍 Man! He/She's hardcore",  # 6-10 solved
            "🐐👑 He/She's a legend!",  # 10+ solved
        ]
        p_choice = preambles[min(int(total / 5), len(preambles) - 1)]
        await ctx.send(f"{p_choice}\n```CSS\n{to_ret}```")

    @stats.command()
    @commands.has_any_role(*(PUNDIT['adminroles']))
    async def top(self, ctx, count):
        """
        Returns top X players
        """
        board = pundit.leaderboard(count=int(count))
        leaderboard = discord.Embed(
            title="Leaderboard",
            description="Leader board for the recruitment tasks",
            color=0xff0000,
        )
        leaderboard.set_footer(
            text="Note: This is an automatically generated report by pundit."
        )
        leaderboard.add_field(
            name="Rank",
            value="\n".join(list(map(
                str,
                list(range(1, count+1)),
            ))),
            inline=True,
        )
        leaderboard.add_field(
            name="user",
            value="\n".join(list(map(
                lambda x: str(self.client.get_user(int(x[0]))).split("#")[0],
                board,
            ))),
            inline=True,
        )
        leaderboard.add_field(
            name="Score",
            value="\n".join(list(map(
                lambda x: str(x[1]),
                board
            ))),
            inline=True,
        )
        await ctx.send(
            embed=leaderboard
        )


def setup(client):
    client.add_cog(Pundit(client))
