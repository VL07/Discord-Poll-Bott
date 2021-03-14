import discord
import threading
import json
import sys

intents = discord.Intents.default()
intents.members = True 


client = discord.Client(intents=intents)

PREFIX = "/"

CHECKROLEPOLLS = {}


def convertParameters(s):
    l = s.split(", ")
    n = ""
    l[0] = l[0].split(" ")[1:]
    for item in l[0]:
        n += item + " "
    l[0] = n
    return l

def savepolls():
    global CHECKROLEPOLLS
    print("saving...")
    f = open("save.json", "w")
    f.write(json.dumps(CHECKROLEPOLLS))
    f.close()
    print("saved...")

def getpolls():
    global CHECKROLEPOLLS
    try:
        f = open("save.json")
        s = f.read()
        CHECKROLEPOLLS = json.loads(s)
        f.close()
        print("read pols")
        print(CHECKROLEPOLLS)
    except:
        print("error on load")





@client.event
async def on_ready():
    global PREFIX
    print(f"{client.user} is now ready!!!")
    await client.change_presence(activity=discord.Game(name=f"{PREFIX}help"))
    getpolls()

async def checkroles():
    print("runing checkroles")

    for key in CHECKROLEPOLLS:

        channel = client.fetch_channel(key)

        message = await channel.fetch_message(CHECKROLEPOLLS[key][messageId])

        reactions = message.reactions

        print(reactions)



@client.event
async def on_message(message):
    global PREFIX
    global CHECKROLEPOLLS
    if message.author != client.user and message.content[0] == PREFIX:
        if message.content.startswith(PREFIX + "np") or message.content.startswith(PREFIX + "normalpoll"):
            parameters = convertParameters(message.content)

            l = []
            for item in parameters:
                if item == "" or item == " " or item == "   " or item == ",":
                    pass
                else:
                    l.append(item)
            
            parameters = l

            if len(parameters) < 3:
                me = f"`{PREFIX}np` takes at least three aguments, `title`, `option 1`, `option 2` you can add more options if you want to"
                embedvar = discord.Embed(title="Error", description=me, color=0xff0000)
                await message.channel.send(embed=embedvar)
                return

            text = ""
            i = 0
            reactions = []
            for item in parameters[1:]:
                text2 = f"{str(i + 1)} {item}\n"
                text += text2.replace("0", "0️⃣").replace("1", "1️⃣").replace("2", "2️⃣").replace("3", "3️⃣").replace("4", "4️⃣").replace("5", "5️⃣").replace("6", "6️⃣").replace("7", "7️⃣").replace("8", "8️⃣").replace("9", "9️⃣")
                reactions.append(str(i + 1).replace("0", "0️⃣").replace("1", "1️⃣").replace("2", "2️⃣").replace("3", "3️⃣").replace("4", "4️⃣").replace("5", "5️⃣").replace("6", "6️⃣").replace("7", "7️⃣").replace("8", "8️⃣").replace("9", "9️⃣"))

                i += 1

            embedvar = discord.Embed(title=parameters[0], description=text, color=0x00ff00)
            embedvar.set_footer(text=f"Poll started by {message.author}", icon_url=message.author.avatar_url)

            m = await message.channel.send(embed=embedvar)

            await message.delete()

            for item in reactions:
                await m.add_reaction(item)

        elif message.content.startswith(PREFIX + "cp") or message.content.startswith(PREFIX + "changeprefix"):
            parameters = message.content.split(" ")[1:]

            if len(parameters) != 1:
                me = f"`{PREFIX}cp` takes one agument, `new prefix`"
                embedvar = discord.Embed(title="Error", description=me, color=0xff0000)
                await message.channel.send(embed=embedvar)
                return
            
            PREFIX = parameters[0]

            embedvar = discord.Embed(title=f"Changed prefix to {parameters[0]}", description=f"Prefix changed by {message.author}", color=0x00ff00)
            await message.channel.send(embed=embedvar)

            await client.change_presence(activity=discord.Game(name=f"{PREFIX}help"))

            await message.delete()

        elif message.content.startswith(PREFIX + "h") or message.content.startswith(PREFIX + "help"):
            
            embedvar = discord.Embed(title="Help", description=f"{message.author} needed some help", color=0x00ff00)
            embedvar.add_field(name="Normal poll", value=f"`{PREFIX}np title, awnser one, awnser two, etc`\n`title`: the poll title, `awnser`: the valid awnsers for the poll", inline=True)
            embedvar.add_field(name="Change prefix", value=f"`{PREFIX}cp new prefix`\n`new prefix`: the new prefix pr all of the commands", inline=True)
            embedvar.add_field(name="Role poll", value=f"`{PREFIX}rp title, awnser one, role one`\n`title`: the poll title, `awnser`: the valid awnsers for the poll, `role`: the role you get when you react with the corresponding role", inline=False)
            embedvar.add_field(name="Sourcecode", value=f"`{PREFIX}source`", inline=True)

            embedvar.set_footer(text=f"If you don't understand ask someone who knows how to use {client.user.name}")
            embedvar.set_author(name=message.author.name, icon_url=message.author.avatar_url)

            await message.channel.send(embed=embedvar)

            await message.delete()

        elif message.content.startswith(PREFIX + "rp") or message.content.startswith(PREFIX + "rolepoll"):
            parameters = convertParameters(message.content)

            if len(parameters) < 3:
                me = f"`{PREFIX}rp` takes at least three aguments, `title`, `option 1`, `role 1` you can add more options if you want to"
                embedvar = discord.Embed(title="Error", description=me, color=0xff0000)
                await message.channel.send(embed=embedvar)
                return

            text = ""
            i = 1
            i2 = 0
            reactions = []
            while i < len(parameters):
                text2 = f"{str(i2 + 1)} {parameters[i]}\n"
                text += text2.replace("0", "0️⃣").replace("1", "1️⃣").replace("2", "2️⃣").replace("3", "3️⃣").replace("4", "4️⃣").replace("5", "5️⃣").replace("6", "6️⃣").replace("7", "7️⃣").replace("8", "8️⃣").replace("9", "9️⃣")
                reactions.append(str(i2 + 1).replace("0", "0️⃣").replace("1", "1️⃣").replace("2", "2️⃣").replace("3", "3️⃣").replace("4", "4️⃣").replace("5", "5️⃣").replace("6", "6️⃣").replace("7", "7️⃣").replace("8", "8️⃣").replace("9", "9️⃣"))

                i += 2
                i2 += 1

            embedvar = discord.Embed(title=parameters[0], description=text, color=0x00ff00)
            embedvar.set_footer(text=f"Poll started by {message.author}", icon_url=message.author.avatar_url)

            m = await message.channel.send(embed=embedvar)

            await message.delete()

            CHECKROLEPOLLS[m.id] = {"emojiid": {}}

            savepolls()

            i = 2
            for item in reactions:
                await m.add_reaction(item)
                CHECKROLEPOLLS[str(m.id)]["emojiid"][item] = parameters[i]
                print("debug: " + str(CHECKROLEPOLLS))
                i += 2

            savepolls()
        
        elif message.content.startswith(PREFIX + "sys.exit"):
            embedvar = discord.Embed(title="Stoping bot", description="The bot will become AFK now", color=0x00ffff)
            embedvar.set_footer(text=f"Bot stoped by {message.author}", icon_url=message.author.avatar_url)

            await message.channel.send(embed=embedvar)

            await message.delete()

            sys.exit()

        elif message.content.startswith(PREFIX + "debug"):
            print("ROLES LIST: " + str(CHECKROLEPOLLS))
            await message.delete()

        elif message.content.startswith(PREFIX + "source"):
            embedvar = discord.Embed(title="Sourse code", description="The bots source code", color=0x00ff00, url="https://github.com/VL07/Discord-Poll-Bott/")
            embedvar.set_footer(text=f"{message.author} wanted the source code", icon_url=message.author.avatar_url)

            await message.channel.send(embed=embedvar)

            await message.delete()


            





            


@client.event
async def on_raw_reaction_add(payload):
    global CHECKROLEPOLLS
    if str(payload.message_id) in CHECKROLEPOLLS.keys():
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)

        print(list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys()))

        if str(payload.emoji) in list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys()):

            print(payload.emoji)
            print(payload.member)

            member = payload.member
            roles = CHECKROLEPOLLS[str(payload.message_id)]["emojiid"]

            print(roles)
            
            role = ""

            print("debug len: " + str(list(roles.values())))
            
            for item in list(roles.keys()):
                print("d: ", str(item), str(payload.emoji))
                if str(item) == str(payload.emoji):
                    role = roles[str(item)]
                    break

            # role = discord.utils.get(discord.guild.Role, id=CHECKROLEPOLLS[payload.message_id]["emojiid"][str(payload.emoji)])
            role = int(role[3:-1])

            print(role)
            print("id=786543498274537472")

            #print(guild.roles)
            role = discord.utils.get(guild.roles, id=role)

            print(role)
            
            await member.add_roles(role)


        else:
            print("not valid emoji: ")
            print(str(list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys())) + str(payload.emoji))

    else:
        print(str(payload.message_id))


@client.event
async def on_raw_reaction_remove(payload):
    global CHECKROLEPOLLS
    if str(payload.message_id) in CHECKROLEPOLLS.keys():
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)

        print(list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys()))

        if str(payload.emoji) in list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys()):

            print(payload.emoji)
            print(payload.member)

            #member = payload.member
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            roles = CHECKROLEPOLLS[str(payload.message_id)]["emojiid"]

            print(roles)
            
            role = ""

            print("debug len: " + str(list(roles.values())))
            
            for item in list(roles.keys()):
                print("d: ", str(item), str(payload.emoji))
                if str(item) == str(payload.emoji):
                    role = roles[str(item)]
                    break

            # role = discord.utils.get(discord.guild.Role, id=CHECKROLEPOLLS[payload.message_id]["emojiid"][str(payload.emoji)])
            role = int(role[3:-1])

            print(role)
            print("id=786543498274537472")

            #print(guild.roles)
            role = discord.utils.get(guild.roles, id=role)

            print(role)
            print(member)
            
            await member.remove_roles(role)


        else:
            print("not valid emoji: ")
            print(str(list(CHECKROLEPOLLS[str(payload.message_id)]["emojiid"].keys())) + str(payload.emoji))

    else:
        print(str(payload.message_id))
        print(CHECKROLEPOLLS)
        print(payload.emoji)


@client.event
async def on_message_delete(message):
    global CHECKROLEPOLLS
    if str(message.id) in CHECKROLEPOLLS.keys():
        print("MESSAGE DELETED")
        CHECKROLEPOLLS.pop(message.id)



getpolls()
client.run("NO TOKEN HERE")
