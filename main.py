import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='&', intents=intents, help_command=None, allowed_mentions=None)

loop = True
tasks = []
remind_task = None

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="only tvesha (&help)"))
    print("bot is ready")
@client.command(aliases=[])
async def help(ctx):
    say_hi = discord.Embed(title=f"hey, {client.user.name} would love to help you out (:", description="type:\n &tasks -your to-do- \n After getting a reminder type &tasks so that the bot doesn't remind you again ", color=discord.Color.from_rgb(5, 179, 173))
    await ctx.send(embed=say_hi)

@client.command(aliases=["end_task"])
async def tasks(ctx,*,tasks_input=None):
    global remind_task
    global tasks
    global loop
    await ctx.trigger_typing()
    try:
        tasks = tasks_input.split(",")
    except:
        if loop:
            loop = False
            remind_task.cancel()
            return await ctx.send("task finished")

        else:

            say_hii = discord.Embed(title=f"hey, {client.user.name} would love to help you out (:",
                                   description="type:\n &tasks -your to-do- \n After getting a reminder type &tasks so that the bot doesn't remind you again ",
                                   color=discord.Color.from_rgb(5, 179, 173))

            return await ctx.send(embed=say_hii)

    time_emb = discord.Embed(description="Please define the intervals you want to be reminded in,, Ex 12 m or 1 hour. (:")
    time_emb.set_footer(text="\nOnly days, hours, minutes, seconds are supported right now. :sweat_smile: \n m, min, minute, minutes is for -minutes.-\n s, sec, seconds is for -seconds-. \n h, hour, hours is for -hours-. \n d, day, days is for -days-")
    time_msg = await ctx.send(embed=time_emb)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    try:
        message = await client.wait_for('message', timeout=120.0, check=check)
    except asyncio.TimeoutError:
        await time_msg.delete()

    else:


            if message.content.endswith("sec") or message.content.endswith("s") or message.content.endswith("seconds"):
                nums = [int(i) for i in message.content.split() if i.isdigit()]
                try:
                    time = nums[0]
                except IndexError:
                    return await ctx.send("enter a frkn digit bruh :smh:")
            elif message.content.endswith("min") or message.content.endswith("minutes") or message.content.endswith("minute") or message.content.endswith("m"):
                nums = [int(i) for i in message.content.split() if i.isdigit()]
                try:
                    time = nums[0]*60
                except IndexError:
                    return await ctx.send("enter a frkn digit bruh :smh:")

            elif message.content.endswith("h") or message.content.endswith("hours") or message.content.endswith("hour"):
                nums = [int(i) for i in message.content.split() if i.isdigit()]
                try:
                    time = nums[0]*3600
                except IndexError:
                    return await ctx.send("enter a frkn digit bruh :smh:")


            elif message.content.endswith("d") or message.content.endswith("days") or message.content.endswith("day"):

                nums = [int(i) for i in message.content.split() if i.isdigit()]

                try:

                    time = nums[0] * 86400

                except IndexError:

                    return await ctx.send("enter a frkn digit bruh :smh:")

            loop = True
            remind_task = client.loop.create_task(remind_back(ctx, time))





async def remind_back(ctx,time):
    global loop

    channel = ctx.channel

    embed = discord.Embed(title="Tasks noted!",
                            description=f"{ctx.author.mention}\n You'll receive all your task reminders here.",
                            color=discord.Color.from_rgb(5, 179, 173))
    embed.set_footer(text="You'll recieve the reminders here.")
    await channel.send(embed=embed)


    while loop:
        await asyncio.sleep(time)
        task_msg = "\n".join(f"{i}. {v}" for i,v in enumerate(tasks,1))
        remind_emb = discord.Embed(title=f"Here's your task list with the remaining tasks for the day,{ctx.author.mention}.",
        description=f"\n{task_msg}\n",color=discord.Color.from_rgb(5, 179, 173))
        await channel.send(embed=remind_emb)

@client.command(aliases=[])
async def add_task(ctx, *, task_input):
    global tasks
    tasks.append(task_input)
    channel = ctx.channel
    t_embed = discord.Embed(title="Tasks added!",
                          description=f"{ctx.author.mention}\n You'll receive all your task reminders here.",
                          color=discord.Color.from_rgb(5, 179, 173))
    t_embed.set_footer(text="You'll recieve the reminders here.")
    await channel.send(embed=t_embed)

@client.command(aliases=[])
async def remove_task(ctx, *, index):
    global tasks
    index = int(index)
    del tasks[index-1]
    channel = ctx.channel
    remove_embed = discord.Embed(title="Tasks removed!",
                            description=f"{ctx.author.mention}\n You'll receive all your task reminders here.",
                            color=discord.Color.from_rgb(5, 179, 173))
    remove_embed.set_footer(text="You'll recieve the reminders here.")
    await channel.send(embed=remove_embed)

@client.command(aliases=[])
async def completed(ctx, *, index):
    global tasks
    index = int(index)
    current = tasks[index-1]
    tasks[index-1] = current + "\✅"
    channel = ctx.channel
    complete_embed = discord.Embed(title="Task(s) completed!",
                            description=f"{ctx.author.mention}\n You'll receive all your other task(s)' reminders here.",
                            color=discord.Color.from_rgb(5, 179, 173))
    await channel.send(embed=complete_embed)


client.run("token")
