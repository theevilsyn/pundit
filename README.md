# Pundit

## Installation

```bash
sudo apt install mysql-server
pip install mosspy
bash init.sh /path/to/dump.sql
git clone https://gitlab.com/theevilsyn/pundit-demo

cd pundit
python3 start.py
```

## Pundit

Update the discord bot's token in `config.yaml`

### Usage

  - `!help` in discord.

### API Calls

  - `http://35.238.186.24:1337/ping`
    - Ping & Pong
  - `http://35.238.186.24:1337/stats/<userid>`
    - Get a user statistics
    - **Example**: `http://35.238.186.24:1337/stats/540599462805110794`
  - `http://35.238.186.24:1337/submit/<userid>/<bashuploadid>/tasks.zip`
    - Submit tasks as a user.
    - **Example**: `http://pundit:1337/submit/540599462805110794/zU28D/tasks.zip`


### config.yaml

```yaml
pundit:
    server: <server-guild-id>
    adminroles:
        - Major General
        - Lieutenant
    admincategories:
        - admins
    playerroles:
        base: 
            - 
                role: Private
                secret: flag{st4rT_y0ur_j0urn3y_1nt0_7h3_d4rk_w0rld}
            -
                role: Private First Class
                secret: flag{f1gh7_y0ur_w4y_1nt0_7h3_dUnG30n5}
        roles:
            500: Sergeant
            1000: Master Sergeant
            1500: Sergeant Major
    mossid: <moss-api-key>
    prefix: !!str "!"
    token: <discord-bot-token>

storage:
    master: /path/to/master/submissions/folder
    repo: github.com/theevilsyn/pundit-demo.git
    token: <git-token>
    database: <database-name>
    db_user: <db-user>
    db_pass: <db-user-password>
```


## Task Validator

### For Challenge Authors
Supported Challenge Types
  - Flag Based
  - Programming Based

This is the format that should be followed for creating a challenge.

TODO
  - restrict a few systemcalls for c and asm tasks

### tasks.yaml

```yaml
sanity:
    name: Sanity Check
    desc: Just the Sanity Check
    value: 100
    flageval: yes
    flag: flag{.*}

summer:
    name: The Summer
    desc: Prints the sum of number given
    value: 200
    flageval: no
    language: python
    allowed: 
        - re
        - string
    maxlines: 0
    delimiter: !!str " "
    testcases:
        sample:
          input: "50 50\n"
          output: "100\n"
        input:
            - [100] 
            - [100, 69]
            - [100, 10, 1]
        output:
            - [100]
            - [169]
            - [111]

swapper:
    name: Swapper
    desc: Sawps the case of the list of strings given
    value: 200
    flageval: no
    language: c
    flags: 
        - "-Wall"
        - "-Werror=format-security"
        - "-fstack-protector-all"
    delimiter: !!str "\n"
    testcases:
        sample:
          input: "2\nbB\ncC\n"
          output: "Bb\nCc\n"
        input:
            - [1, aa]
            - [2, bB, cC]
            - [3, dd, ee, ff]
        output:
            - [AA]
            - [Bb, Cc]
            - [DD, EE, FF]
```
**Refer [tasks.yaml](./tasks.yaml) for more accurate instructions**
### For Players

All the tasks must be zipped in the following structure

```
- tasks.zip
  - swapper/
    - swapper.py
  - summer/
    - summer.c
    - Makefile
  - sanity/
    - sanity.flag
    - sanity.txt
```

Make the zip file downloadable from the internet and give the link to pundit

Ex. 
`!tasks submit https://bashupload.com/Nb-Kb/tasks.zip`

All the python files must take the testcase input from stdin and print the respective output to stdout.

The flag evaluated solutions should be named `task.flag` with the contents `flag{.*}` i.e, the respective flag.

