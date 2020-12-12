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
        value=10,
        description=
        """
        Write a python program to print the text `Hello World!`
        """,
        sampleoutput="Hello World!"
    )

def mapping():
    return createEmbed(
        name="Mapping",
        value=90,
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
        value=100,
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
        value=100,
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
        value=100,
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
Harry"""
    )

def ginortS():
    return createEmbed(
        name="ginortS",
        value=100,
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

def athletesort():
    return createEmbed(
        name="Athlete Sort",
        value=100,
        description="""
        You are given details that contains a list of `N` athletes and their details (such as age, height, weight and so on). You are required to sort the data based on the `Kth` attribute and print the final resulting table.
        Note that `K` is indexed from `0` to `M-1` , where `M` is the number of attributes.
        Note: If two attributes are the same for different rows, for example, if two atheletes are of the same age, print the row that appeared first in the input.

        **Input Format:**
        The first line contains `N` and `M` separated by a space.
        The next `N` lines each contain `M` elements.
        The last line contains `K`.

        **Output Format:**
        Print the `N` lines of the sorted table. Each line should contain the space separated elements.""",
        sampleinput=
"""
5 3
10 2 5
7 1 0
9 9 9
1 23 12
6 5 9
1
""",
        sampleoutput=
"""
7 1 0
10 2 5
6 5 9
9 9 9
1 23 12
""",
        image_url="https://s3.amazonaws.com/hr-assets/0/1514874268-6fabad07aa-AthleteSort2.png",
        explanation="Follow the example in the above image for better understanding."
    )

def trichop():
    return createEmbed(
        name="Triangle Chopsticks",
        value=100,
        description=
        """
        Natsu and Grey are having a silly fight again and this time it's about the person who is going to have the larger piece of pie. So the guild master gives them a puzzle to solve and announces that the winner gets the larger pie. There are 2 chopsticks with some given lengths 'a' and 'b' and a jar with chopsticks of different lengths. Grey is going to pick a random number 'r' and Natsu is going to check if it is possible to make a triangle considering each chopstick from the jar as the 3rd side and finds the total count of triangles that can be formed. If the no.of triangles formed is more than the random number then Natsu is going to win. Else Grey wins. So find out the winner. 'n' stands for the no.of test cases.

        **Input Format:**
        First line contains a, b and r
        Second contains the no.of chopsticks in the jar (is always greater than r)
        Third line contains all the lengths of chopsticks in the jar

        **Output Format:**
        In the first line give the total no.of triangles possible
        In the second line give the name of the winner
        """,
        sampleinput=
"""
9 8 4
7
11 14 19 2 8 17 5
""",
        sampleoutput=
"""
5
Natsu
"""
    )

def passfail():
    return createEmbed(
        name="Pass or Fail",
        value=120,
        description=
        """
        Make a program such that it takes input of marks (out of 100) of 'n' subjects along with names of 'm' students. Then it should print the
        names of all the students according to their ranks. The criteria for ranking is based on averages. Also, the student who scored less than 40
        in any of the subjects is not eligible for ranking and is considered 'FAIL'. Make sure to print the list of students who failed in atleast
        one of the subjects.

        **Input Format:**
            Line one : n,m separated with space
            m times:
                Line one : student name
                Line two : his marks separated with space


        **Output Format:**
            Line one : A dictionary of keys as ranks and values as names
            Line two : list of students failed in at least one subject sorted by alphabetical order
        """,
        sampleinput=
"""
7 5
Joe
53 77 68 63 71 71 68
Wesley
59 53 57 70 86 46 95
Lita
44 63 50 40 58 89 81
Randal
91 64 69 84 46 72 54
Sibyl
43 35 41 55 68 39 70
""",
        sampleoutput=
"""
{1: 'Randal', 2: 'Joe', 3: 'Wesley', 4: 'Lita'}

['Sibyl']
"""
    )

def jumbledletters():
    return createEmbed(
        name="Jumbled Letters",
        value=80,
        description=
        """
        Natsu and Lucy were given an assignment in their school. They were given a sentence, all the spaces of it were to be removed, then segregate all the even placed characters, reverse them and add it to the previously left odd characters. They wanted to find the fast way to get the solution and wanted to code it in python. So aren’t you going to help them out?

        **Input Format:**
        The input string

        **Output Format:**
        String formed after the changes
        """,
        sampleinput=
"""
I'm an American.
""",
        sampleoutput=
"""
I.manimerAcan'
"""
    )

def secretimages():
    return createEmbed(
        name="Secret Images",
        value=50,
        description=
        """
        Zeref wants to get hold of secret information of Natsu and he comes to know that it was stored in a list of images. So as a first step he wants to find the no.of images of each extension of from given input. Help him in finding the solution.

        **Input Format:**
        First line contains the file names seperated by space

        **Output Format:**
        Line containing the space seperated integers which are the count of PNG, BMP, JPEG images respectively
        """,
        sampleinput="file0.jpeg file1.png file2.bmp file3.jpeg file4.bmp file5.jpeg",
        sampleoutput="1 2 3"
    )

def readingemails():
    return createEmbed(
        name="Reading Emails",
        value=120,
        description=
"""
**Hunt for the correct ID**
An email ID consists of 3 parts: <local-part>@<domain-part>.<extension>

**The local-part of a valid email address can have:**
    **1**.uppercase and lowercase letters (A-Z, a-z)
    **2**.digits 0-9
    **3**.valid special characters: !#$%^&*{}|~_+-=/' .Whereas '.' is valid only if it's not first and last character.
    **4**.It’s length must not exceed 64 characters.


**The domain-part of the email address can have:**
    **1**.uppercase and lowercase letters (A-Z,a-z)
    **2**.'-' is allowed only if it's the first or last character
    **3**.digits between 0-9 but domain cannot be entirely numeric
    **4**.special symbols are not allowed in the domain
The maximum length of the extension allowed here is 3 and must not have any special characters. Email address verification are usually used for data validation. Well, there are other techniques better than this one but this is the basic one of them.So take the email as input and check if it is valid or not.
""",
        sampleinput="email@example.museum",
        sampleoutput="False"
    )

def leapyear():
    return createEmbed(
        name="Leap Year",
        value=100,
        description=
        """
        I was wondering about a friend of mine, a leap year baby. Being just 4 years old (ambiguous), we had a fun party. We decided it then to stretch his birthday timeline in a line. Between, his birthday years seemed complex.
        Give me the best algorithm to check for leap years.
        
        Here is the catch: Complete your submission in one line. That is, without using external libraries or methods, define the complete function and the return statement in one line of code to prove your worth.
        """,
        sampleinput="2933",
        sampleoutput="False"
    )

def tribonnaci():
    return createEmbed(
        name="Tribonacci Series",
        value=90,
        description=
        """
        The **tribonacci numbers** are like the Fibonacci numbers, but instead of starting with two predetermined terms, the sequence starts with three predetermined terms and each term afterwards is the sum of the preceding three terms. The first few tribonacci numbers are:
        0, 0, 1, 1, 2, 4, 7, 13, 24, 44,81, 149, 274, 504, 927
        1 : 1
        2 : 1,2
        4 : 1,2,4
        7 : 1,7
        13 : 1,13
        24 : 1,2,3,4,6,8,12,24

        We can see that 24 is the first Tribonacci number to have over 7 divisors.
        What is the value of the first Tribonacci number to have over N divisors?
        """,
        sampleinput="7",
        sampleoutput="24"
    )

def minimax():
    return createEmbed(
        name="Mini Max",
        value=40,
        description=
        """
        Given n positive integers, find the minimum and maximum values that can be calculated by summing exactly n-1 of the n integers. Then print the respective minimum and maximum values as a single line of two space-separated long integers.
        **Explanation:**
        Our initial numbers are 1,2,3,4, and 5. We can calculate the following sums using four of the five integers:
            1. If we sum everything except 1, our sum is 14.
            2. If we sum everything except 2, our sum is 13.
            3. If we sum everything except 3, our sum is 12.
            4. If we sum everything except 4, our sum is 11.
            5. If we sum everything except 5, our sum is 10.
		**Input Format**:
		A single line of n space separated integers.
		**Output Format**:
		Print two space-separated long integers denoting the respective minimum and maximum values that can be calculated by summing exactly n-1 of the n integers. (The output can be greater than a 32 bit integer.)
        """,
        sampleinput="331 651 992 196 435 180 263",
        sampleoutput="2036 2848"
    )

def equateascii():
    return createEmbed(
        name="Equate Ascii",
        value=50,
        description=
        """
        Here your main goal is to the given two words sare some string(string is the combiantion of cahrecters).
        So here we have to equate them by equating the ascii of the given string .
        So here you should make the out put such that after you run the code the person should get to known the ascii value of the given both string are equal
        
        For example:
        ascii value of "abc" will be like = 97+98+99 = 295.
        So you have to write the code such that it checks that the given two strings are equal
        """,
        sampleinput="Allena Anjelica",
        sampleoutput="False"
    )

def caesargame():
    return createEmbed(
        name="Caesar's Game",
        value=150,
        description=
        """
        My friends and I have develped a secret code to communicate with each other. If you wanna be a part of us you should do the following task.

        Your task is to create two functions :
        1.First function should create the secret code from the given English text
        2.Second function should decode the secret code back to plain English text

        **Input Format:**
        First line should contain the number they chose.
        Second line should be a number 0 or 1 (0 to encrypt and 1 to decrypt)
        Third line should contain the sentence for encryption/decryption.

        **Output Format:**
        One line which would display the encrypted/decrypted text .
        """,
        sampleinput=
"""
14
1
I think I'm going crazy.
""",
        sampleoutput=
"""
u ftuzw u'y sauzs odmlk.
"""
    )

SECONDCHALLS = [
    athletesort,
    trichop,
    passfail,
    jumbledletters,
    secretimages,
    readingemails,
    leapyear,
    tribonnaci,
    minimax,
    equateascii,
    caesargame,
]
# SECONDCHALLS = [minimax]

async def sendchalls(client):
    taskChnl = get(
            get(
                client.get_guild(id=787331336813412353).categories, name='general'
            )
            .channels,
            name='sergeant-tasks'
        )
    for task in SECONDCHALLS:
        await taskChnl.send(
            embed=task()
        )
    return

def createEmbed(name="", value="", description="", sampleinput="", sampleoutput="", explanation="", image_url=""):
    challenge = discord.Embed(
        title=name+"\n"+f"Points: {value}",
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
    if(image_url):
        challenge.set_image(url=image_url)
    return challenge

@client.event
async def on_ready():
    await sendchalls(client)
client.run("Nzg3MzMxNDU3NTgzOTM5NTk0.X9TZjw.PTn1oDyD4Kq7uzcCda7haOav-04")