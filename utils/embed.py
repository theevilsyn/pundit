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
Harsh"""
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

def passorfail():
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
            Line two : list of students failed in at least one subject
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
        An email ID consists of 3 parts: @.
        The local-part of a valid email address can have:
            1.uppercase and lowercase letters (A-Z, a-z)
            2.digits 0-9
            3.valid special characters: !#$%^&*{}|~_+-=/' .Whereas '.' is valid only if it's not first and last character.
            4.It’s length must not exceed 64 characters.
        The domain-part of the email address can have:
            1.uppercase and lowercase letters (A-Z,a-z)
            2.'-' is allowed only if it's the first or last character
            3.digits between 0-9 but domain cannot be entirely numeric
            4.special symbols are not allowed in the domain
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

def trinonnaci():
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

        **Input Format:**
        First line T, the number of testcases. Each testcase consists of N in one line.
        **Output Format:**
        For each testcase, print the required answer in one line.
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
        Given five positive integers, find the minimum and maximum values that can be calculated by summing exactly four of the five integers. Then print the respective minimum and maximum values as a single line of two space-separated long integers.
        **Explanation:**
        Our initial numbers are 1,2,3,4, and 5. We can calculate the following sums using four of the five integers:
            1. If we sum everything except 1, our sum is 14.
            2. If we sum everything except 2, our sum is 13.
            3. If we sum everything except 3, our sum is 12.
            4. If we sum everything except 4, our sum is 11.
            5. If we sum everything except 5, our sum is 10.
        **Input Format:**
        A single line of five space  separated integers.
        **Output Format:**
        Print two space-separated long integers denoting the respective minimum and maximum values that can be calculated by summing exactly four of the five integers. (The output can be greater than a 32 bit integer.)
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
        For example :
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

        Input :
        First line should contain the number they chose.
        Second line should be a number 0 or 1 (0 to encrypt and 1 to decrypt)
        Third line should contain the sentence for encryption/decryption.

        Output :
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
U ftuzw U'y sauzs odmlk.
"""
    )

def Integers():
    return createEmbed(
        name="Integers",
        value=400,
        description=
        """
        Pointers are pretty important in c. A thing clarifying pointers would be nice.
        So try to implement the python `int()` function in C.
        Like `atoi(char* ptr, int base)` to return the integer
        stored at the pointer ptr.

        The function accepts a pointer to a string and an integer mode as arguments and
        utputs the appropriate number.

        The format should be `Int(char* numstring, int base)`
```
Example:
    Int(‘234234234’, 10)
    Output: 234234234
    Int(‘64’, 16)
    Output: 40
```


        **This task should be implemented in C language**
        **Difficulty: Medium**
        """,
        sampleinput=
"""
64
16
""",
        sampleoutput=
"""
40
"""
    )

def Print():
    return createEmbed(
        name="Print This",
        value=600,
        description=
        """
        **Implement a function `“print_this”` in C which is the equivalent of the printf in C.**
        **1.** The function should accept a format string and the number of arguments as specified by the format string.
        **2.** The function should be able to accept and process:
        **a.**Strings -eg `print_this(“%s”,ptr)` should print ptr as a string
        **b.** Hex numbers -eg `print_this(“%x”, 10)` should print `0xa`
        **c.**Octal numbers
        **d.**Binary numbers
        **3.** `%p`, `%u`, `%d` should all be handled
        **4.**Numbers before like `%02d` should be used to specify bytes printed on the screen.
        **5.**%$ should be treated as a illegal format string that cannot be used and print_this should print nothing and return an error.
        An `EACCESS` error must be returned.
        **6.** Should print other illegal escape sequences directly
        **7.** The function should not use printf. It can use putc to print to the screen.
        **8.** The function should be available to use by other programs. Write a header file so that other functions can import this function.
        **9.** Macros must be used to denote any integer values used inside thefunction.
        **10.** The function should also return proper values to denote that the execution happened properly
        **11.** Also make sure that the number of arguments passed is same as the number of the format strings present.
        Incase this is not same the function should return some error.
        **12.** Feel free to add any good modifications that you feel will bebeneficial for yourself and the community.


        **This task should be implemented in C-lang**
        **Difficulty: Hard**
        """,
        sampleinput=
"""
hello, world!
""",
        sampleoutput=
"""
hello, world!
"""
    )

def maximus():
    return createEmbed(
        name="Maximus Optimus",
        value=160,
        description=
        """
        Fox, Alex are playing a game called Addition Game. Three numbers A, B and C are written on a blackboard, and Alex initially has 0 points. He repeats the following operation exactly N times: He chooses one of the three numbers on the blackboard. Let X be the chosen number. He gains X points, and if X >= 1, the number X on the blackboard becomes X-1. Otherwise, the number does not change. Print the maximum number of points he can gain if he plays optimally.

        **Input Format:**
        3 numbers and the number of times the game repeats
        **Output Format:**
        Maximum number of points possible for the inputs


        **This task should be implemented in C language**
        """,
        sampleinput=
"""
3
4
5
3
""",
        sampleoutput=
"""
13
"""
    )

def Nostring():
    return createEmbed(
        name="No String",
        value=40,
        description=
        """
        Write a program in C to compare two string without using string library functions and prints which line ("First" or "Second") is shorter or "Equal" if they are equal.

        **Input Format:**
        This is first string
        This is first string

        **Output Format:**
        Equal

        **This task should be implemented in C language**
        **Difficulty: Easy**
        """,
        sampleinput=
"""
aaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
""",
        sampleoutput=
"""
First
"""
    )

def Pointers():
    return createEmbed(
        name="Pointers Assemble",
        value=70,
        description=
        """
        Write a program in C to sort an array using pointers.

        **This task should be implemented in C language**
        """,
        sampleinput=
"""
5
25
45
89
15
82
""",
        sampleoutput=
"""
15
25
45
82
89
"""
    )

def Teacher():
    return createEmbed(
        name="Teachers Secrets",
        value=120,
        description=
        """
        Your teacher proposes the following quick method of evaluating the correctness of the answer to an exam question. She writes down several distinct keywords she expects to find in a correct answer. Each keyword has a score associated with it. She then searches for each keyword in the student’s answer. If she finds it, she adds the score of the keyword to the student's score. If she finds the keyword multiple times, she only adds its score once.


    You are given a keywords and a scores. The ith element of keywords contains the ith keyword. The ith element of scores gives the score associated with the ith keyword. You are also given a answer with the student's answer. answer will be a single-space delimited list of words. Return the final score the student will receive for his answer.

    **Input Format:**
    An Integer containing number keywords
    An array of string containing the keywords
    An array of integer containing the marks allotted for each keyword
    A string containing the answer provided by the student

    **Output Format:**
    The marks obtained by the student


    **This task should be implemented in C language**
        """,
        sampleinput=
"""
4
red fox lazy dogs
25 25 25 25
the quick brown fox jumped over the lazy dog
""",
        sampleoutput=
"""
50
"""
    )

def Toget10():
    return createEmbed(
        name="Toget10",
        value=110,
        description=
        """
        You are given an integer array containing the grades you have received so far in a class. Each grade is between 0 and 10, inclusive. Assuming that you will receive a 10 on all future assignments, determine the minimum number of future assignments that are needed for you to receive a final grade of 10. You will receive a final grade of 10 if your average grade is 9.5 or higher.

        **Input:**
        First line is an integer showing number of previous assignment
        Second line is the space seperated array of integers containing the marks of previous assignment

        **Output:**
        The minimum number of future assignments required


        **This task should be implemented in C language**
        """,
        sampleinput=
"""
2
8 9
""",
        sampleoutput=
"""
4
"""
    )

def roxy():
    return createEmbed(
        name="Roxy",
        value=150,
        category="Crypto",
        description=
        """
        In this some data is appended and pre-appended to the flag string to form a new string which contains the flag. Consequently this new string is xored.

        Your goal is recover the flag from the given xored ciphertext.

        **Flag Format**: `inctf{some string}`

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1QshxkPyk3vQKsUFP8_aBy8Sjin02UrL2/view?usp=sharing
            Mirror 2: https://mega.nz/file/B7QAyLDb#_1Y-xXb9MsvQgjivr2hk_JgOP9Z9Vn5kFXtegdrbo2c 
        """
    )

def mysimplecipher():
    return createEmbed(
        name="My Simple Cipher",
        value=250,
        category="Crypto",
        description=
        """
        So in this challenge we have two unknowns the key and the flag and u are given the output of the program i.e the ciphertext. Your goal is to find the flag. But for that u will need the key. Carefully analyse the operations being done on the flag to generate the ciphertext. Note the use of modulus means things will repeat. Make use of this repetioon to crack the challenge.
        
        **Flag format**: `TWCTF{some_string}`

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1jbnzNb2HXIYOwd8xwKKNqgab7L_Z2Yl5/view?usp=sharing
            Mirror 2: https://mega.nz/file/EyYEBbhb#sMqckNg2hTjy-9wjl8Fsdolq32PrpBeShFO6lXT4TSM
        """
    )

def welcometoassembly():
    return createEmbed(
        name="Welcome to Assembly",
        value=150,
        category="Reverse",
        description=
        """
        If the value in DWORD PTR [ebp+0x8] is 0x76. What will be the value in register eax just before the program terminates. 
        
        **Flag format**: `flag{some_hexadecimal(0x)_value}`
        
        **Hint**: Assembly Tutorial - https://www.cs.virginia.edu/~evans/cs216/guides/x86.html

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1IEG3LfJ179sud4RAmq4CWMk70P6anwtw/view?usp=sharing
            Mirror 2: https://mega.nz/file/kvQCGLAb#2jcq287EWTOzazWD1rNL_tpwnYBAj93qiad5qGIgIfo
        """
    )

def re_chall2():
    return createEmbed(
        name="Scrabble",
        value=250,
        category="Reverse",
        description=
        """
        Inside this vault there is a secret. Our agency wants you to break through this vault. Dr. Hecker sabotaged the source code to make it hard for our agents but I believe only you can do it.

        **Flag Format**: `flag{somestring}`

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1cY27MmvkazzCmTNFP9BLjoJ-QKUSfezf/view?usp=sharing
            Mirror 2: https://mega.nz/file/ZyYQEZCR#izdZiUSZ0u3ow59RKCPFTprPEdUZTyyzWBbOI5PiEig
        """
    )

def buggypp():
    return createEmbed(
        name="Buggy-PHP",
        value=250,
        category="Web",
        description=
        """
        Exploit bugs, Capture flags !

        **Flag Format**: `inctfj{some_l33t_string}`

        **Challenge Link**: http://168.119.123.141:9898/

        **Hint**: Are you sure its an [A](https://en.wikipedia.org/wiki/Unicode)?
        """
    )

def warmup():
    return createEmbed(
        name="Warmup",
        value=150,
        category="Web",
        description=
        """
        Find the "SOURCE" of the problems :P

        **Flag Format**: `inctfj{some_l33t_string}`

        **Challenge Link**: http://168.119.123.141:6070/
        """
    )

def devhack():
    return createEmbed(
        name="Development Hack",
        value=150,
        category="Hardware",
        description=
        """
	Solve the logic gates and decipher the circuit.

        **Challenge File**: https://drive.google.com/drive/folders/1v0GpyAW2AWoRshXviGqycJWZvLeUd7gT?usp=sharing

        **Flag Format**: `flag{FLAG=..}`
        """
    )

def hwsniff():
    return createEmbed(
        name="7 sniff",
        value=250,
        category="Hardware",
        description=
        """
	While testing our hardware challenge we tapped the communication happening between 7 segment display and a shift register and obtained some data, but due to a faulty display, we were unable to see the flag. Find a way to use the code to display the flag on 7-segment. Hint - Tinkercad loves LSB first.

        **Challenge File**: https://drive.google.com/drive/folders/1Ln1ZkNol8hfm1ChaEn3tOQgdSN-V1DPQ?usp=sharing

        **Flag Format**: `flag{FLAG=..}`
        """
    )

def for1():
    return createEmbed(
        name="Over the shark",
        value=150,
        category="Forensics",
        description=
        """
        Can you find the hidden data from this recording? 
        
        **Note**: You need to crack the zip password.

        **Flag Format**: `actf{some string}`

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1JcHyOri1RmyXhYz8AAw73ld7IMEAxTSN/view?usp=sharing
            Mirror 2: https://mega.nz/file/FyhEhAwI#73Dl2NCQ29U71iBxTwp40QPkKpDGXGHzLy8BgY2nPvE
        """
    )

def for2():
    return createEmbed(
        name="Critical",
        value=250,
        category="Forensics",
        description=
        """
        Ravi sent me this file and said there is something interesting in this. But I am not able to open this file. Can you help me in recovering this file.
        
        **Note**: You need to crack the zip password.

        **Flag Format**: `inctf{some_string}`

        **Challenge File**:
            Mirror 1: https://drive.google.com/file/d/1wP4hrZU4fYZG2VHEuGPn5uWjbT1j538W/view?usp=sharing
            Mirror 2: https://mega.nz/file/w2oCjAgK#T1cNEXnBsuxFAAfNImSSkJfq1ye-_a3EArONL_JU_5Y
        """
    )

SECONDCHALLS = [
    # athletesort,
    #trichop,
    # passorfail,
    # jumbledletters,
    # secretimages
    #readingemails,
    #leapyear,
    #trinonnaci,
    #minimax,
    #equateascii,
    #caesargame,
    #Integers, # master
    #Print, # master
    # maximus,
    # Nostring,
    # Pointers,
    # Teacher,
    # Toget10
    #roxy,
    #mysimplecipher,
    #welcometoassembly,
    #re_chall2,
    buggypp,
    #warmup,
    #devhack,
    #hwsniff,
    for1,
    for2,
]

async def sendchalls(client):
    # taskChnl = get(
    #         get(
    #             client.get_guild(id=760306433374814277).categories, name='admins'
    #         )
    #         .channels,
    #         name='bot-testing'
    #     )
    taskChnl = client.get_channel(id = 760352099090432020)
    for task in SECONDCHALLS:
        await taskChnl.send(
            embed=task()
        )
    return

def createEmbed(name="", value="", description="", category="", sampleinput="", sampleoutput="", explanation="", image_url=""):
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
    if(category):
        challenge.add_field(
            name="Category",
            value=category,
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
    exit(0)
client.run("NzUzODUxNzI2OTE3OTI3MDA1.X1sNIQ.YWc5hCwt3k-aS8N8llagN83cdLc")
