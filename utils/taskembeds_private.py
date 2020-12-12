import random
from time import sleep

import discord
from discord.ext import commands, tasks
from discord.utils import get

# from core.pundit.pundit import PUNDIT

client = commands.Bot(command_prefix=commands.when_mentioned_or(
    'j!'), description='Nah!!')

def hello():
    return createEmbed(
        name="Hello World!",
        description=
        """
        Write a python program to print the text `Hello World!`
        """,
        sampleoutput="Hello World!"
    )

def mapping():
    return createEmbed(
        name="Mapping",
        description=
        """
        Write a small python program to take a few numbers as input and make them print as a list
        """,
        sampleinput="1 22 33 44",
        sampleoutput="[1, 22, 33, 44]"
    )

def multiply():
    return createEmbed(
        name="Multiply",
        description=
        """
        Write a small python program to take a few <space> seperated numbers as input and make the product of those numbers
        """,
        sampleinput="10 20 30 100",
        sampleoutput="600000",
        explanation="""
Explanation:
10*20*30*100 = 600000
"""
    )

def allorany():
    return createEmbed(
        name="All or Any",
        description=
        """
        You are given a space separated list of integers. If all the integers are positive, then you need to check if any integer is a palindromic integer.
        Note: Single Digit Numbers are always palindromic
            **Input Format**
                The first line contains the space separated list of integers.

            **Output Format**
                Print "True" if all the conditions of the problem statement are satisfied. Otherwise, print "False".
        """,
        sampleinput="12 9 61 5 14",
        sampleoutput="True",
        explanation=
        """
Explanation:
Condition 1: All the integers should be positive (True)
Condition 2: Atleast one of the integers must be palindromic (True)
Since both the conditions are passed that prints "True"
"""
    )

def nlists():
    return createEmbed(
        name="Nested Lists",
        description=
        """
        Given the names and grades for each student in a class of  students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.
        Note: If there are multiple students with the second lowest grade, order their names alphabetically and print each name on a new line.
            **Input Format:**
                The first line contains an integer, specifying the number of students.
                The  subsequent lines describe each student over lines.
                - The first line contains a student's name.
                - The second line contains their grade.
            **Constraints:**
            There will always be one or more students having the second lowest grade.

            Output Format:
            Print the name(s) of any student(s) having the second lowest grade in. If there are multiple students, order their names alphabetically and print each one on a new line."
        """,
        sampleinput=
        """
5
Harry
37.21
Berry
37.21
Tina
37.2
Akriti
41
Harsh
39""",
        sampleoutput=
        """
Berry
Harsh"""
    )

def ginortS():
    return createEmbed(
        name="ginorts",
        description=
        """
        You are given a string S.
        S contains alphanumeric characters only.
        Your task is to sort the string  in the following manner
        All sorted lowercase letters are ahead of uppercase letters.
        All sorted uppercase letters are ahead of digits.
        All sorted odd digits are ahead of sorted even digits.
            **Input Format:**
            A single line of input contains the string .

            **Output Format:**
            Output the sorted string .
        """,
        sampleinput="Sorting1234",
        sampleoutput="ginortS1324"

    )


CHALLS = [
    hello,
    mapping,
    multiply,
    allorany,
    nlists,
    ginortS,
]

# def 

# SECONDCHALLS = [

# ]

async def sendchalls(client):
    taskChnl = get(
            get(
                client.get_guild(id=787331336813412353).categories, name='general'
            )
            .channels,
            name='tasks'
        )
    for task in CHALLS:
        await taskChnl.send(
            embed=task()
        )
    return

def createEmbed(name="", description="", sampleinput="", sampleoutput="", explanation=""):
    challenge = discord.Embed(
        title=name,
        description=description,
        color=0xff0000
    )
    if(sampleinput):
        challenge.add_field(
            name="Sample Input",
            value='```'+sampleinput+'```',
        )
    if(sampleoutput):
        challenge.add_field(
            name="Sample Output",
            value='```'+sampleoutput+'```',
        )
    if(explanation):
        challenge.set_footer(
            text=explanation
        )

    return challenge

@client.event
async def on_ready():
    await sendchalls(client)
client.run("Nzg3MzMxNDU3NTgzOTM5NTk0.X9TZjw.PTn1oDyD4Kq7uzcCda7haOav-04")